"""Tickets: one folder each, the moves the line allows, the red checks, and the gate.

Sub-agents write their results into the ticket folder as files. This module is
the only writer of ticket.json. It refuses a move the line does not allow, so
the order of the stages does not depend on anyone remembering it.
"""

import fcntl
import hashlib
import json
import os
import re
import shutil
import subprocess
import tempfile
import time
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path

STAGES = ("intake", "research", "verification", "build", "review", "done")
# Where a ticket may go from each stage. Review is missing from build on purpose:
# only the gate moves a ticket there.
MOVES = {
    "intake": ("research", "verification"),
    "research": ("verification", "done"),
    "verification": ("build", "research"),
    "build": ("verification", "research"),
    "review": ("build", "done", "verification", "research"),
    "done": (),
}
# "done" is not a state the caller sets. A ticket is done when its stage is done.
SETTABLE_STATES = ("working", "waiting", "stopped")
KINDS = ("standard", "research")
# Rounds of build, gate, review a ticket gets before the line stops and asks Levi.
ROUND_LIMIT = 4
GATE_TIMEOUT_SECONDS = 1800
GATE_TAIL_LINES = 60
# The verifier's files: the plan, the script the gate runs, and anything that script calls, kept in checks/.
# They are hashed when the build starts. The gate refuses to run if any changed, appeared, or went missing since.
LOCKED_FILES = ("verification-plan.md", "checks.sh")
CHECKS_FOLDER = "checks"
# A red check is a script in checks/ that must fail before the build and pass after it.
# It proves the check can tell broken from fixed. The plan says why under this heading when it has none.
RED_CHECKS = "red-*.sh"
RED_SECTION = "red first"
# Files a parent ticket hands to a ticket opened to build one of its solutions.
INHERITED_FILES = ("request.md", "levi.md", "solution.md")
TOP_FILE_ORDER = ("request.md", "levi.md", "solution.md", "plan.md", "verification-plan.md", "checks.sh", "red.md", "red.log")
ROUND_FILE_ORDER = ("build.md", "gate.md", "gate.log", "review.md")
SLUG_LENGTH = 40
TICKET_ID = re.compile(r"^[a-z0-9][a-z0-9-]*$")
# The only shapes of path the board will read from a ticket folder.
# Documents sit at the top or in a round folder. Helper scripts for the checks sit in checks/ and may be code.
FILE_PATH = re.compile(
    r"^((round-[0-9]+/)?[a-z][a-z0-9-]*\.(md|sh|log)"
    r"|checks/[A-Za-z0-9][A-Za-z0-9_.-]*\.(md|sh|py|js|ts|rb|go|json|txt|sql|yaml|yml|csv))$"
)
# The line a sub-agent puts first in its file, such as `REVIEW: ACCEPT`.
VERDICT_LINE = re.compile(r"^[A-Z-]+: [A-Z-]+$")
FILE_BYTES_SHOWN = 200000
SUMMARY_LINES_SHOWN = 6
# Fields every command reads. A ticket file without them is unreadable.
REQUIRED_FIELDS = ("id", "title", "stage", "state", "rounds", "updated", "updates")


class FactoryError(Exception):
    """A failure the caller can fix, or a move the line refuses. The CLI prints it and exits non-zero."""


def factory_home():
    override = os.environ.get("SOFTWARE_FACTORY_HOME")
    return Path(override) if override else Path.home() / ".software-factory"


def tickets_dir():
    return factory_home() / "tickets"


def utc_now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def slugify(title):
    """A short id from the title. It is cut between words, so the id never ends on half a word."""
    slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    if len(slug) > SLUG_LENGTH:
        slug = slug[: SLUG_LENGTH + 1].rsplit("-", 1)[0]
    return slug[:SLUG_LENGTH] or "ticket"


def one_line(text, field):
    """Titles and notes are shown on one line. Blank ones would show as an empty card."""
    cleaned = " ".join(text.split())
    if not cleaned:
        raise FactoryError("%s is empty" % field)
    return cleaned


# ---- Storage ----------------------------------------------------------------


def ticket_folder(ticket_id):
    # The id becomes a path, so it is checked before it is joined to one.
    if not TICKET_ID.match(ticket_id):
        raise FactoryError("ticket id may only hold lowercase letters, digits, and hyphens: %r" % ticket_id)
    return tickets_dir() / ticket_id


def read_ticket(ticket_id):
    path = ticket_folder(ticket_id) / "ticket.json"
    try:
        ticket = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise FactoryError("no ticket named %r under %s" % (ticket_id, tickets_dir()))
    except ValueError as err:
        raise FactoryError("ticket file is not valid JSON: %s (%s)" % (path, err))
    missing = [field for field in REQUIRED_FIELDS if not isinstance(ticket, dict) or field not in ticket]
    if missing:
        raise FactoryError("ticket file is missing %s: %s" % (", ".join(missing), path))
    return ticket


def write_ticket(ticket):
    # Write to a file of its own, then swap it in, so the board never reads half a ticket.
    folder = ticket_folder(ticket["id"])
    handle, scratch = tempfile.mkstemp(dir=str(folder), prefix="ticket-", suffix=".tmp")
    with os.fdopen(handle, "w", encoding="utf-8") as out:
        out.write(json.dumps(ticket, indent=2) + "\n")
    os.replace(scratch, folder / "ticket.json")


@contextmanager
def ticket_lock(ticket_id):
    """One writer at a time per ticket. Without it, two updates read the same file and one is lost."""
    folder = ticket_folder(ticket_id)
    if not folder.is_dir():
        raise FactoryError("no ticket named %r under %s" % (ticket_id, tickets_dir()))
    with open(folder / "ticket.lock", "w") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        yield


def load_tickets():
    """Every ticket that can be read, and the ids of the ones that cannot."""
    tickets, unreadable = [], []
    folders = sorted(tickets_dir().iterdir()) if tickets_dir().is_dir() else []
    for folder in folders:
        if not (folder / "ticket.json").is_file():
            continue
        try:
            tickets.append(read_ticket(folder.name))
        except FactoryError:
            unreadable.append(folder.name)
    return tickets, unreadable


def append_update(ticket, note):
    ticket["updated"] = utc_now()
    ticket["updates"].append(
        {"at": ticket["updated"], "stage": ticket["stage"], "state": ticket["state"], "note": note}
    )


# ---- Files the sub-agents leave ---------------------------------------------


def first_line(path):
    """The verdict line a sub-agent puts at the top of its file. None when the file is not there."""
    try:
        with path.open(encoding="utf-8", errors="replace") as lines:
            return lines.readline().strip()
    except OSError:
        return None


def round_folder(ticket, number=None):
    return ticket_folder(ticket["id"]) / ("round-%d" % (ticket["rounds"] if number is None else number))


def section_of(path, heading):
    """The lines under `## <heading>` in a sub-agent's file, without the blank ones."""
    try:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return []
    found, inside = [], False
    for line in lines:
        if line.startswith("## "):
            if inside:
                break
            inside = line.strip().lower() == "## " + heading
        elif inside and line.strip():
            found.append(line.strip())
    return found


def summary_of(path):
    """The bullets under `## Summary`, which every sub-agent file carries for the human and the orchestrator."""
    return section_of(path, "summary")[:SUMMARY_LINES_SHOWN]


def file_rank(name, order):
    # Files the line does not name, such as a scout's, sit right after Levi's answers.
    return order.index(name) if name in order else 1.5


def list_files(ticket_id):
    """Every document in the ticket folder, in the order the line produces them."""
    folder = ticket_folder(ticket_id)
    top = [p for p in folder.iterdir() if p.is_file() and FILE_PATH.match(p.name)]
    ordered = sorted(top, key=lambda p: (file_rank(p.name, TOP_FILE_ORDER), p.name))
    rounds = [d for d in folder.glob("round-*") if d.is_dir() and d.name[6:].isdigit()]
    for subfolder in [folder / CHECKS_FOLDER] + sorted(rounds, key=lambda d: int(d.name[6:])):
        if not subfolder.is_dir():
            continue
        inside = [p for p in subfolder.iterdir() if p.is_file() and FILE_PATH.match("%s/%s" % (subfolder.name, p.name))]
        ordered += sorted(inside, key=lambda p: (file_rank(p.name, ROUND_FILE_ORDER), p.name))
    return [{"path": str(p.relative_to(folder)), "first_line": first_line(p)} for p in ordered]


def read_file(ticket_id, relative):
    """One document from a ticket folder, for the board. Long logs are cut to their end."""
    if not FILE_PATH.match(relative):
        raise FactoryError("not a ticket document: %r" % relative)
    path = ticket_folder(ticket_id) / relative
    try:
        data = path.read_bytes()
    except OSError:
        raise FactoryError("no such document in ticket %s: %s" % (ticket_id, relative))
    text = data[-FILE_BYTES_SHOWN:].decode("utf-8", errors="replace")
    if len(data) > FILE_BYTES_SHOWN:
        text = "(showing the last %d bytes of %d)\n\n%s" % (FILE_BYTES_SHOWN, len(data), text)
    return text


def round_results(ticket):
    """What each round's files say, for the board: READY, PASS, REJECT and so on."""

    def verdict(path):
        line = first_line(path)
        return line.split(":", 1)[1].strip() if line and ":" in line else None

    results = []
    for number in range(1, ticket["rounds"] + 1):
        folder = round_folder(ticket, number)
        results.append(
            {
                "round": number,
                "build": verdict(folder / "build.md"),
                "gate": verdict(folder / "gate.md"),
                "review": verdict(folder / "review.md"),
            }
        )
    return results


def status_text(ticket_id):
    """The ticket's stage and what every file says, so the orchestrator need not open the files."""
    ticket = read_ticket(ticket_id)
    folder = ticket_folder(ticket_id)
    lines = [
        "%s: %s" % (ticket["id"], ticket["title"]),
        "kind: %s | stage: %s | state: %s | round: %d of %d"
        % (ticket.get("kind") or "not set", ticket["stage"], ticket["state"], ticket["rounds"], round_limit(ticket)),
        "target: %s" % (ticket.get("target") or "not set"),
        "folder: %s" % folder,
    ]
    for document in list_files(ticket_id):
        lines.append("")
        # Only a sub-agent's file opens with a verdict. The first line of a script or a log is noise here.
        verdict = document["first_line"] if VERDICT_LINE.match(document["first_line"] or "") else None
        lines.append("%s: %s" % (document["path"], verdict) if verdict else document["path"])
        lines += ["  %s" % bullet for bullet in summary_of(folder / document["path"])]
    return "\n".join(lines)


# ---- Opening a ticket, and Levi's words --------------------------------------


def claim_ticket_folder(base_id):
    """Create a folder no other ticket has. mkdir fails if another session got there first."""
    tickets_dir().mkdir(parents=True, exist_ok=True)
    suffix = 1
    while True:
        ticket_id = base_id if suffix == 1 else "%s-%d" % (base_id, suffix)
        try:
            (tickets_dir() / ticket_id).mkdir()
            return ticket_id
        except FileExistsError:
            suffix += 1


def create_ticket(title, request, target, parent=None):
    """Open a ticket. A ticket opened under a parent builds one of the parent's solutions."""
    title = one_line(title, "title")
    parent_ticket = read_ticket(parent) if parent else None
    if not parent_ticket and not (request or "").strip():
        raise FactoryError("request is empty")
    now = utc_now()
    # The id carries the calendar date Levi sees, so it uses local time. Timestamps are UTC.
    ticket_id = claim_ticket_folder("%s-%s" % (datetime.now().strftime("%Y-%m-%d"), slugify(title)))
    folder = ticket_folder(ticket_id)
    ticket = {
        "id": ticket_id,
        "title": title,
        "target": target,
        "parent": parent,
        "kind": None,
        "stage": "intake",
        "state": "working",
        "rounds": 0,
        "round_limit": ROUND_LIMIT,
        "locked": {},
        "created": now,
        "updated": now,
        "updates": [{"at": now, "stage": "intake", "state": "working", "note": "Ticket opened."}],
    }
    if parent_ticket:
        # The solution is already chosen, so this ticket starts where research ends.
        for name in INHERITED_FILES:
            source = ticket_folder(parent) / name
            if source.is_file():
                shutil.copyfile(str(source), str(folder / name))
        ticket.update(kind="research", stage="research")
        ticket["updates"][0].update(stage="research", note="Opened to build one solution of %s." % parent)
    else:
        (folder / "request.md").write_text("# Request\n\n%s\n" % request.strip(), encoding="utf-8")
    write_ticket(ticket)
    return ticket


def record_levi(ticket_id, about, words):
    """Append what Levi said, verbatim, so every sub-agent reads his words and not a retelling."""
    about = one_line(about, "about")
    if not words.strip():
        raise FactoryError("Levi's words are empty")
    with ticket_lock(ticket_id):
        path = ticket_folder(ticket_id) / "levi.md"
        if not path.exists():
            path.write_text(
                "# Levi's answers and decisions\n\nIn his words. A later entry overrides an earlier one.\n",
                encoding="utf-8",
            )
        with path.open("a", encoding="utf-8") as out:
            out.write("\n## %s (%s)\n\n%s\n" % (about, utc_now(), words.strip()))
    return path


# ---- Moves ------------------------------------------------------------------


def round_limit(ticket):
    return ticket.get("round_limit", ROUND_LIMIT)


def children_of(ticket_id):
    tickets, _ = load_tickets()
    return [ticket for ticket in tickets if ticket.get("parent") == ticket_id]


def require_first_line(path, expected, then):
    found = first_line(path)
    if found == expected:
        return
    saw = "It is missing." if found is None else "It starts with `%s`." % found
    raise FactoryError("refused: %s must start with `%s`. %s %s" % (path.name, expected, saw, then))


def check_move(ticket, stage):
    """Raise unless the line allows this ticket to move to `stage` now."""
    current, folder = ticket["stage"], ticket_folder(ticket["id"])
    if stage == "review":
        raise FactoryError("refused: only the gate moves a ticket to review. Run `gate %s`." % ticket["id"])
    if stage not in MOVES[current]:
        allowed = ", ".join(MOVES[current]) or "nowhere"
        raise FactoryError("refused: a ticket cannot move from %s to %s. From %s it can go to: %s." % (current, stage, current, allowed))
    if stage == "research" and ticket["kind"] != "research":
        raise FactoryError("refused: only a research task goes to research. Pass --kind research with the move.")
    if current == "intake" and stage == "verification" and ticket["kind"] != "standard":
        raise FactoryError("refused: only a standard task skips research. Set --kind first. A research task goes to research.")
    if current == "research" and stage == "verification":
        require_first_line(folder / "plan.md", "PLAN: READY", "Research ends with a plan for the solution Levi chose.")
    if current == "research" and stage == "done":
        children = children_of(ticket["id"])
        if not children or any(child["stage"] != "done" for child in children):
            raise FactoryError("refused: a ticket leaves research as done only when it has solution tickets and each one is done.")
    if current == "verification" and stage == "build":
        require_first_line(folder / "verification-plan.md", "VERIFICATION: READY", "The build needs the verification plan first.")
        if not ticket["rounds"]:
            require_red(ticket)
    if current == "review" and stage == "build":
        require_first_line(round_folder(ticket) / "review.md", "REVIEW: REJECT", "A ticket returns to build when the reviewer rejects.")
    if current == "review" and stage == "done":
        require_first_line(round_folder(ticket) / "review.md", "REVIEW: ACCEPT", "A ticket is done when the reviewer accepts.")


def file_hash(path):
    try:
        return hashlib.sha256(path.read_bytes()).hexdigest()
    except OSError:
        return None  # not there. A plan with no automated checks has no checks.sh


def verifier_files(ticket_id):
    """The hash of each file the build is judged by, keyed by its path in the ticket folder."""
    folder = ticket_folder(ticket_id)
    hashes = {name: file_hash(folder / name) for name in LOCKED_FILES}
    helpers = folder / CHECKS_FOLDER
    for path in sorted(helpers.rglob("*")) if helpers.is_dir() else []:
        if path.is_file():
            hashes[str(path.relative_to(folder))] = file_hash(path)
    return hashes


def require_red(ticket):
    """Raise unless the red checks were confirmed on the verifier's files as they are now."""
    red = ticket.get("red") or {}
    if red.get("files") != verifier_files(ticket["id"]):
        why = "changed since the red checks ran" if red else "not been tried against the code as it is today"
        raise FactoryError("refused: the checks have %s. Run `red %s` before the first build." % (why, ticket["id"]))
    if red.get("verdict") == "NOT-RED":
        raise FactoryError(
            "refused: a red check passes before the build, so it cannot tell broken from fixed: see red.md. "
            "The verifier fixes the check, then run `red %s` again." % ticket["id"]
        )


def start_round(ticket):
    """Open the next round's folder. Refuses once the ticket has used its rounds."""
    if ticket["rounds"] >= round_limit(ticket):
        raise FactoryError(
            "refused: %d rounds ended without an accept. Mark the ticket stopped and tell Levi what is in the way. "
            "If he says to keep going, pass --more-rounds." % ticket["rounds"]
        )
    ticket["rounds"] += 1
    round_folder(ticket).mkdir(exist_ok=True)


def apply_move(ticket, stage):
    check_move(ticket, stage)
    if stage == "build":
        start_round(ticket)
        if ticket["stage"] == "verification":
            # From here the implementer builds to these files, so they may not change under it.
            ticket["locked"] = verifier_files(ticket["id"])
    ticket["stage"] = stage


def update_ticket(ticket_id, note, stage=None, state=None, kind=None, title=None, target=None, more_rounds=False):
    note = one_line(note, "note")
    if stage == "done" and state:
        raise FactoryError("a done ticket cannot also be %s" % state)
    with ticket_lock(ticket_id):
        ticket = read_ticket(ticket_id)
        if kind:
            ticket["kind"] = kind
        if title is not None:
            ticket["title"] = one_line(title, "title")
        if target is not None:
            ticket["target"] = target
        if more_rounds:
            ticket["round_limit"] = round_limit(ticket) + ROUND_LIMIT
        if stage and stage != ticket["stage"]:
            apply_move(ticket, stage)
        # An update means someone is working, unless the caller says the ticket is waiting or stopped.
        ticket["state"] = "done" if ticket["stage"] == "done" else (state or "working")
        append_update(ticket, note)
        write_ticket(ticket)
    return ticket


def save_usage(ticket_id, usage):
    """Keep a done ticket's cost on the ticket. Claude Code deletes old transcripts."""
    with ticket_lock(ticket_id):
        ticket = read_ticket(ticket_id)
        ticket["usage"] = usage
        write_ticket(ticket)


# ---- Red first --------------------------------------------------------------


def red_checks(ticket_id):
    return sorted((ticket_folder(ticket_id) / CHECKS_FOLDER).glob(RED_CHECKS))


def run_red_checks(ticket, checks, timeout):
    """Run each red check in the target. Returns (path in the ticket folder, exit code) pairs. None means it never finished."""
    folder = ticket_folder(ticket["id"])
    env = dict(os.environ, TICKET_FOLDER=str(folder), ROUND="0")
    results = []
    with (folder / "red.log").open("w", encoding="utf-8") as out:
        for check in checks:
            name = str(check.relative_to(folder))
            out.write("== %s\n" % name)
            out.flush()
            try:
                code = subprocess.run(
                    ["bash", str(check)], cwd=ticket["target"], env=env, stdout=out, stderr=subprocess.STDOUT, timeout=timeout
                ).returncode
            except subprocess.TimeoutExpired:
                code = None
            results.append((name, code))
    return results


def red_outcome(code, timeout):
    if code is None:
        return "did not finish in %d seconds, so it proves nothing" % timeout
    if code == 0:
        return "passed. It cannot tell broken from fixed"
    return "failed (exit %d), as it must" % code


def write_red_report(ticket, verdict, results, reason, timeout):
    folder = ticket_folder(ticket["id"])
    if verdict == "NONE":
        (folder / "red.log").write_text("", encoding="utf-8")
        summary = ["- The plan has no red checks, so nothing was run", "- The verifier's reason: %s" % " ".join(reason)]
        detail = []
    else:
        failed = sum(1 for _, code in results if code)
        tail = (folder / "red.log").read_text(encoding="utf-8", errors="replace").splitlines()[-GATE_TAIL_LINES:]
        summary = [
            "- %d of %d red checks failed before the build. Every one must" % (failed, len(results)),
            "- Run in %s, on the code as it is before the build" % ticket["target"],
            "- Full output: red.log, beside this file",
        ]
        rows = ["| `%s` | %s |" % (name, red_outcome(code, timeout)) for name, code in results]
        detail = ["", "## Red checks", "", "| Red check | Before the build |", "| --- | --- |"] + rows
        detail += ["", "## Last lines of the output", "", "```"] + tail + ["```"]
    report = ["RED: %s" % verdict, "", "## Summary"] + summary + detail + [""]
    (folder / "red.md").write_text("\n".join(report), encoding="utf-8")


def red(ticket_id, timeout=GATE_TIMEOUT_SECONDS):
    """Before the first build, run each red check and confirm it fails. Returns (verdict, ticket)."""
    with ticket_lock(ticket_id):
        ticket = read_ticket(ticket_id)
        folder = ticket_folder(ticket_id)
        if ticket["stage"] != "verification" or ticket["rounds"]:
            raise FactoryError(
                "refused: red checks run in verification, before the first build. This ticket is in %s, round %d. "
                "Once a build has started the code is no longer broken, so they cannot be tried."
                % (ticket["stage"], ticket["rounds"])
            )
        plan = folder / "verification-plan.md"
        require_first_line(plan, "VERIFICATION: READY", "Red checks run on a finished plan.")
        checks, files, reason = red_checks(ticket_id), verifier_files(ticket_id), section_of(plan, RED_SECTION)
        if checks:
            if not ticket.get("target") or not Path(ticket["target"]).is_dir():
                raise FactoryError("refused: the ticket's target is not a folder: %r. Set it with --target." % ticket.get("target"))
            script = folder / "checks.sh"
            wired = script.read_text(encoding="utf-8", errors="replace") if script.is_file() else ""
            unwired = [check.name for check in checks if check.name not in wired]
            if unwired:
                raise FactoryError(
                    "refused: checks.sh does not call %s. A red check must fail before the build and pass at the gate, "
                    "so checks.sh has to run it." % ", ".join(unwired)
                )
        elif not reason:
            raise FactoryError(
                "refused: the plan has no red check and does not say why. The verifier adds a red check in checks/, "
                "or gives the reason under `## Red first` in the plan."
            )

    # The checks can run for minutes. The lock is not held, so progress notes still land.
    results = run_red_checks(ticket, checks, timeout) if checks else []
    verdict = "NONE" if not checks else ("CONFIRMED" if all(code for _, code in results) else "NOT-RED")

    with ticket_lock(ticket_id):
        ticket = read_ticket(ticket_id)
        if ticket["stage"] != "verification" or ticket["rounds"] or verifier_files(ticket_id) != files:
            raise FactoryError("the ticket or its checks changed while the red checks ran. Their result was not recorded.")
        write_red_report(ticket, verdict, results, reason, timeout)
        ticket["red"] = {"verdict": verdict, "files": files}
        ticket["state"] = "working"
        note = {
            "CONFIRMED": "Red checks confirmed: %d failed before the build, as they must. The build is next." % len(results),
            "NOT-RED": "A red check did not fail before the build: see red.md. Back to the verifier.",
            "NONE": "The plan has no red checks and says why. The build is next.",
        }[verdict]
        append_update(ticket, note)
        write_ticket(ticket)
    return verdict, ticket


# ---- The gate ---------------------------------------------------------------


def check_locked_files(ticket):
    locked, now = ticket.get("locked", {}), verifier_files(ticket["id"])
    changed = sorted(name for name in set(locked) | set(now) if locked.get(name) != now.get(name))
    if changed:
        raise FactoryError(
            "refused: %s changed after the build started. Only the verifier changes the plan and the checks. "
            "Move the ticket to verification, have the verifier confirm them, then move it back to build." % ", ".join(changed)
        )


def run_checks(ticket, timeout):
    """Run the ticket's checks.sh in the target. Returns (passed, one line saying what happened)."""
    folder, round_dir = ticket_folder(ticket["id"]), round_folder(ticket)
    checks, log = folder / "checks.sh", round_dir / "gate.log"
    if not checks.is_file():
        log.write_text("", encoding="utf-8")
        return True, "The plan has no automated checks, so there was nothing to run"
    env = dict(os.environ, TICKET_FOLDER=str(folder), ROUND=str(ticket["rounds"]))
    started = time.time()
    with log.open("w", encoding="utf-8") as out:
        try:
            code = subprocess.run(
                ["bash", str(checks)], cwd=ticket["target"], env=env, stdout=out, stderr=subprocess.STDOUT, timeout=timeout
            ).returncode
        except subprocess.TimeoutExpired:
            return False, "checks.sh did not finish in %d seconds and was stopped" % timeout
    return code == 0, "checks.sh exited %d after %d seconds" % (code, time.time() - started)


def write_gate_report(ticket, passed, happened):
    round_dir = round_folder(ticket)
    tail = (round_dir / "gate.log").read_text(encoding="utf-8", errors="replace").splitlines()[-GATE_TAIL_LINES:]
    report = [
        "GATE: %s" % ("PASS" if passed else "FAIL"),
        "",
        "## Summary",
        "- %s" % happened,
        "- Round %d. Run in %s" % (ticket["rounds"], ticket["target"]),
        "- Full output: gate.log, beside this file",
        "",
        "## Last lines of the output",
        "",
        "```",
    ]
    (round_dir / "gate.md").write_text("\n".join(report + tail + ["```", ""]), encoding="utf-8")


def gate(ticket_id, timeout=GATE_TIMEOUT_SECONDS):
    """Run the checks and move the ticket: to review on a pass, to the next round on a fail."""
    with ticket_lock(ticket_id):
        ticket = read_ticket(ticket_id)
        if ticket["stage"] != "build":
            raise FactoryError("refused: the gate runs on a ticket in build. This one is in %s." % ticket["stage"])
        require_first_line(round_folder(ticket) / "build.md", "BUILD: READY", "The gate runs when the implementer says the build is ready.")
        check_locked_files(ticket)
        if not ticket.get("target") or not Path(ticket["target"]).is_dir():
            raise FactoryError("refused: the ticket's target is not a folder: %r. Set it with --target." % ticket.get("target"))
        this_round = ticket["rounds"]

    # The checks can run for minutes. The lock is not held, so progress notes still land.
    passed, happened = run_checks(ticket, timeout)

    with ticket_lock(ticket_id):
        ticket = read_ticket(ticket_id)
        if ticket["stage"] != "build" or ticket["rounds"] != this_round:
            raise FactoryError("the ticket moved while the gate ran. Its result was not recorded.")
        write_gate_report(ticket, passed, happened)
        ticket["state"] = "working"
        if passed:
            ticket["stage"] = "review"
            note = "Gate passed in round %d. The reviewer is next." % this_round
        else:
            note = "Gate failed in round %d: see round-%d/gate.md. Back to the implementer." % (this_round, this_round)
            try:
                start_round(ticket)
            except FactoryError:
                ticket["state"] = "stopped"
                note = "Gate failed in round %d, the last round this ticket has. The line stopped." % this_round
        append_update(ticket, note)
        write_ticket(ticket)
    return passed, ticket
