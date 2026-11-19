"""Tests for the ticket rules, the gate, and the cost reader.

Run from this folder:  python3 -m unittest test_factory
"""

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import tickets
import usage
from tickets import FactoryError

HERE = Path(__file__).parent


class FactoryCase(unittest.TestCase):
    """Each test gets its own factory home, target folder, and Claude config folder."""

    def setUp(self):
        self.scratch = tempfile.TemporaryDirectory()
        self.addCleanup(self.scratch.cleanup)
        root = Path(self.scratch.name)
        self.target = root / "target"
        self.target.mkdir()
        self.claude = root / "claude"
        for name, value in (("SOFTWARE_FACTORY_HOME", root / "home"), ("CLAUDE_CONFIG_DIR", self.claude)):
            previous = os.environ.get(name)
            os.environ[name] = str(value)
            self.addCleanup(self.restore, name, previous)

    @staticmethod
    def restore(name, previous):
        if previous is None:
            os.environ.pop(name, None)
        else:
            os.environ[name] = previous

    def open_ticket(self, title="Fix the cart", kind="standard"):
        ticket = tickets.create_ticket(title, "Checkout returns 500 on an empty cart.", str(self.target))
        if kind:
            tickets.update_ticket(ticket["id"], "Sorted.", kind=kind)
        return ticket["id"]

    def put(self, ticket_id, name, first_line, body="\n## Summary\n- one thing\n"):
        path = tickets.ticket_folder(ticket_id) / name
        path.parent.mkdir(exist_ok=True)
        path.write_text(first_line + "\n" + body, encoding="utf-8")
        return path

    def checks(self, ticket_id, script):
        (tickets.ticket_folder(ticket_id) / "checks.sh").write_text(script, encoding="utf-8")

    def to_build(self, ticket_id, script="exit 0\n"):
        """Take a standard ticket to the start of round 1."""
        tickets.update_ticket(ticket_id, "Verifying.", stage="verification")
        self.put(ticket_id, "verification-plan.md", "VERIFICATION: READY")
        self.checks(ticket_id, script)
        return tickets.update_ticket(ticket_id, "Building.", stage="build")

    def refused(self, *args, **kwargs):
        with self.assertRaises(FactoryError) as caught:
            tickets.update_ticket(*args, **kwargs)
        return str(caught.exception)


class OpeningTickets(FactoryCase):
    def test_request_is_saved_as_a_file_for_sub_agents_to_read(self):
        ticket_id = self.open_ticket()
        request = (tickets.ticket_folder(ticket_id) / "request.md").read_text()
        self.assertIn("Checkout returns 500 on an empty cart.", request)

    def test_two_tickets_with_one_title_get_different_folders(self):
        self.assertNotEqual(self.open_ticket(), self.open_ticket())

    def test_a_long_title_is_cut_between_words(self):
        self.assertEqual(tickets.slugify("Cache supplier price lookups to save cost"), "cache-supplier-price-lookups-to-save")
        self.assertEqual(tickets.slugify("x" * 60), "x" * 40)
        self.assertEqual(tickets.slugify("!!!"), "ticket")

    def test_blank_title_and_blank_request_are_rejected(self):
        with self.assertRaises(FactoryError):
            tickets.create_ticket("   ", "x", "")
        with self.assertRaises(FactoryError):
            tickets.create_ticket("A title", "  ", "")

    def test_a_ticket_id_cannot_reach_outside_the_tickets_folder(self):
        with self.assertRaises(FactoryError):
            tickets.read_ticket("../../etc")


class Moves(FactoryCase):
    def test_a_ticket_cannot_skip_from_intake_to_build(self):
        self.assertIn("cannot move from intake to build", self.refused(self.open_ticket(), "x", stage="build"))

    def test_a_ticket_with_no_kind_cannot_leave_intake(self):
        ticket_id = self.open_ticket(kind=None)
        self.assertIn("standard task", self.refused(ticket_id, "x", stage="verification"))
        self.assertIn("research task", self.refused(ticket_id, "x", stage="research"))

    def test_build_is_refused_until_the_verification_plan_is_ready(self):
        ticket_id = self.open_ticket()
        tickets.update_ticket(ticket_id, "Verifying.", stage="verification")
        self.assertIn("It is missing", self.refused(ticket_id, "x", stage="build"))
        self.put(ticket_id, "verification-plan.md", "VERIFICATION: NEEDS-LEVI")
        self.assertIn("VERIFICATION: NEEDS-LEVI", self.refused(ticket_id, "x", stage="build"))
        self.put(ticket_id, "verification-plan.md", "VERIFICATION: READY")
        ticket = tickets.update_ticket(ticket_id, "Building.", stage="build")
        self.assertEqual((ticket["stage"], ticket["rounds"]), ("build", 1))
        self.assertTrue((tickets.ticket_folder(ticket_id) / "round-1").is_dir())

    def test_only_the_gate_moves_a_ticket_to_review(self):
        ticket_id = self.open_ticket()
        self.to_build(ticket_id)
        self.assertIn("only the gate", self.refused(ticket_id, "x", stage="review"))

    def test_done_needs_the_reviewer_to_accept(self):
        ticket_id = self.open_ticket()
        self.to_build(ticket_id)
        self.put(ticket_id, "round-1/build.md", "BUILD: READY")
        tickets.gate(ticket_id)
        self.assertIn("It is missing", self.refused(ticket_id, "x", stage="done"))
        self.put(ticket_id, "round-1/review.md", "REVIEW: REJECT")
        self.assertIn("REVIEW: REJECT", self.refused(ticket_id, "x", stage="done"))
        self.put(ticket_id, "round-1/review.md", "REVIEW: ACCEPT")
        ticket = tickets.update_ticket(ticket_id, "Accepted.", stage="done")
        self.assertEqual((ticket["stage"], ticket["state"]), ("done", "done"))
        self.assertIn("cannot move from done", self.refused(ticket_id, "x", stage="build"))

    def test_a_reject_starts_the_next_round_and_an_accept_does_not(self):
        ticket_id = self.open_ticket()
        self.to_build(ticket_id)
        self.put(ticket_id, "round-1/build.md", "BUILD: READY")
        tickets.gate(ticket_id)
        self.put(ticket_id, "round-1/review.md", "REVIEW: ACCEPT")
        self.assertIn("REVIEW: ACCEPT", self.refused(ticket_id, "x", stage="build"))
        self.put(ticket_id, "round-1/review.md", "REVIEW: REJECT")
        ticket = tickets.update_ticket(ticket_id, "Rejected.", stage="build")
        self.assertEqual((ticket["stage"], ticket["rounds"]), ("build", 2))

    def test_research_needs_a_plan_before_verification(self):
        ticket_id = self.open_ticket(kind="research")
        self.assertIn("standard task", self.refused(ticket_id, "x", stage="verification"))
        tickets.update_ticket(ticket_id, "Researching.", stage="research")
        self.assertIn("plan.md", self.refused(ticket_id, "x", stage="verification"))
        self.put(ticket_id, "plan.md", "PLAN: READY")
        self.assertEqual(tickets.update_ticket(ticket_id, "Planned.", stage="verification")["stage"], "verification")

    def test_a_standard_task_becomes_a_research_task_only_with_its_kind_changed(self):
        ticket_id = self.open_ticket()
        tickets.update_ticket(ticket_id, "Verifying.", stage="verification")
        self.assertIn("--kind research", self.refused(ticket_id, "x", stage="research"))
        ticket = tickets.update_ticket(ticket_id, "Needs a decision.", stage="research", kind="research")
        self.assertEqual(ticket["stage"], "research")

    def test_waiting_is_cleared_by_the_next_update(self):
        ticket_id = self.open_ticket()
        self.assertEqual(tickets.update_ticket(ticket_id, "Asked Levi.", state="waiting")["state"], "waiting")
        self.assertEqual(tickets.update_ticket(ticket_id, "He answered.")["state"], "working")


class TheGate(FactoryCase):
    def test_the_gate_waits_for_the_implementer_to_report_ready(self):
        ticket_id = self.open_ticket()
        self.to_build(ticket_id)
        with self.assertRaises(FactoryError) as caught:
            tickets.gate(ticket_id)
        self.assertIn("BUILD: READY", str(caught.exception))

    def test_a_pass_moves_the_ticket_to_review_and_records_the_output(self):
        ticket_id = self.open_ticket()
        self.to_build(ticket_id, "echo checks ran in $(basename $PWD)\n")
        self.put(ticket_id, "round-1/build.md", "BUILD: READY")
        passed, ticket = tickets.gate(ticket_id)
        self.assertTrue(passed)
        self.assertEqual((ticket["stage"], ticket["rounds"]), ("review", 1))
        report = (tickets.ticket_folder(ticket_id) / "round-1" / "gate.md").read_text()
        self.assertTrue(report.startswith("GATE: PASS\n"))
        self.assertIn("checks ran in target", report)

    def test_a_fail_keeps_the_ticket_in_build_and_opens_the_next_round(self):
        ticket_id = self.open_ticket()
        self.to_build(ticket_id, "echo the cart test failed; exit 3\n")
        self.put(ticket_id, "round-1/build.md", "BUILD: READY")
        passed, ticket = tickets.gate(ticket_id)
        self.assertFalse(passed)
        self.assertEqual((ticket["stage"], ticket["rounds"], ticket["state"]), ("build", 2, "working"))
        report = (tickets.ticket_folder(ticket_id) / "round-1" / "gate.md").read_text()
        self.assertTrue(report.startswith("GATE: FAIL\n"))
        self.assertIn("exited 3", report)
        self.assertIn("the cart test failed", report)

    def test_checks_that_never_finish_fail_the_gate(self):
        ticket_id = self.open_ticket()
        self.to_build(ticket_id, "sleep 30\n")
        self.put(ticket_id, "round-1/build.md", "BUILD: READY")
        passed, _ = tickets.gate(ticket_id, timeout=1)
        self.assertFalse(passed)

    def test_the_gate_refuses_when_the_checks_changed_after_the_build_started(self):
        ticket_id = self.open_ticket()
        self.to_build(ticket_id, "exit 1\n")
        self.put(ticket_id, "round-1/build.md", "BUILD: READY")
        self.checks(ticket_id, "exit 0\n")  # the weakened check an implementer might leave
        with self.assertRaises(FactoryError) as caught:
            tickets.gate(ticket_id)
        self.assertIn("checks.sh changed", str(caught.exception))

    def test_deleting_the_checks_does_not_pass_the_gate(self):
        ticket_id = self.open_ticket()
        self.to_build(ticket_id, "exit 1\n")
        self.put(ticket_id, "round-1/build.md", "BUILD: READY")
        (tickets.ticket_folder(ticket_id) / "checks.sh").unlink()
        with self.assertRaises(FactoryError):
            tickets.gate(ticket_id)

    def test_a_helper_script_the_checks_call_is_locked_too(self):
        ticket_id = self.open_ticket()
        tickets.update_ticket(ticket_id, "Verifying.", stage="verification")
        self.put(ticket_id, "verification-plan.md", "VERIFICATION: READY")
        self.checks(ticket_id, "python3 \"$TICKET_FOLDER/checks/probe.py\"\n")
        probe = self.put(ticket_id, "checks/probe.py", "import sys", "sys.exit(1)\n")
        tickets.update_ticket(ticket_id, "Building.", stage="build")
        self.put(ticket_id, "round-1/build.md", "BUILD: READY")
        probe.write_text("import sys\nsys.exit(0)\n")  # the probe an implementer made pass
        with self.assertRaises(FactoryError) as caught:
            tickets.gate(ticket_id)
        self.assertIn("checks/probe.py changed", str(caught.exception))
        probe.write_text("import sys\nsys.exit(1)\n")
        self.put(ticket_id, "checks/extra.py", "pass")  # a file slipped in beside it
        with self.assertRaises(FactoryError) as caught:
            tickets.gate(ticket_id)
        self.assertIn("checks/extra.py changed", str(caught.exception))

    def test_the_specialist_can_change_the_checks_by_going_back_through_verification(self):
        ticket_id = self.open_ticket()
        self.to_build(ticket_id, "exit 1\n")
        tickets.update_ticket(ticket_id, "The check was wrong.", stage="verification")
        self.checks(ticket_id, "exit 0\n")
        ticket = tickets.update_ticket(ticket_id, "Plan confirmed.", stage="build")
        self.put(ticket_id, "round-%d/build.md" % ticket["rounds"], "BUILD: READY")
        self.assertTrue(tickets.gate(ticket_id)[0])

    def test_a_plan_with_no_automated_checks_passes_with_nothing_run(self):
        ticket_id = self.open_ticket()
        tickets.update_ticket(ticket_id, "Verifying.", stage="verification")
        self.put(ticket_id, "verification-plan.md", "VERIFICATION: READY")
        tickets.update_ticket(ticket_id, "Building.", stage="build")
        self.put(ticket_id, "round-1/build.md", "BUILD: READY")
        passed, _ = tickets.gate(ticket_id)
        self.assertTrue(passed)
        self.assertIn("no automated checks", (tickets.ticket_folder(ticket_id) / "round-1" / "gate.md").read_text())

    def test_the_line_stops_after_its_rounds_and_continues_when_levi_says_so(self):
        ticket_id = self.open_ticket()
        self.to_build(ticket_id, "exit 1\n")
        for number in range(1, tickets.ROUND_LIMIT + 1):
            self.put(ticket_id, "round-%d/build.md" % number, "BUILD: READY")
            _, ticket = tickets.gate(ticket_id)
        self.assertEqual((ticket["rounds"], ticket["state"]), (tickets.ROUND_LIMIT, "stopped"))
        ticket = tickets.update_ticket(ticket_id, "Levi said keep going.", more_rounds=True)
        self.assertEqual(ticket["round_limit"], 2 * tickets.ROUND_LIMIT)


class FilesInTheFolder(FactoryCase):
    def test_files_are_listed_in_the_order_the_line_makes_them(self):
        ticket_id = self.open_ticket()
        self.to_build(ticket_id)
        self.put(ticket_id, "round-1/build.md", "BUILD: READY")
        self.put(ticket_id, "scout-cart.md", "SCOUT: DONE")
        tickets.gate(ticket_id)
        listed = [(f["path"], f["first_line"]) for f in tickets.list_files(ticket_id)]
        self.assertEqual(
            [path for path, _ in listed],
            ["request.md", "scout-cart.md", "verification-plan.md", "checks.sh", "round-1/build.md", "round-1/gate.md", "round-1/gate.log"],
        )
        self.assertIn(("round-1/gate.md", "GATE: PASS"), listed)

    def test_the_board_can_only_read_documents_inside_the_ticket(self):
        ticket_id = self.open_ticket()
        self.assertIn("Checkout returns 500", tickets.read_file(ticket_id, "request.md"))
        for path in ("../other/request.md", "ticket.json", "round-1/../../x.md", "/etc/passwd", "round-1/deep/x.md", "checks/../ticket.json", ".hidden.md"):
            with self.assertRaises(FactoryError):
                tickets.read_file(ticket_id, path)

    def test_status_shows_each_files_verdict_and_summary(self):
        ticket_id = self.open_ticket()
        tickets.update_ticket(ticket_id, "Verifying.", stage="verification")
        self.put(ticket_id, "verification-plan.md", "VERIFICATION: READY", "\n## Summary\n- three checks\n- one eval\n\n## Checks\n- not a summary line\n")
        status = tickets.status_text(ticket_id)
        self.assertIn("verification-plan.md: VERIFICATION: READY", status)
        self.assertIn("- three checks", status)
        self.assertNotIn("not a summary line", status)

    def test_levis_words_are_kept_verbatim_and_in_order(self):
        ticket_id = self.open_ticket()
        tickets.record_levi(ticket_id, "Which solution", "go with B, but keep the ttl short")
        tickets.record_levi(ticket_id, "Staleness", "5 minutes max")
        saved = (tickets.ticket_folder(ticket_id) / "levi.md").read_text()
        self.assertLess(saved.index("go with B, but keep the ttl short"), saved.index("5 minutes max"))

    def test_round_results_come_from_the_files(self):
        ticket_id = self.open_ticket()
        self.to_build(ticket_id, "exit 1\n")
        self.put(ticket_id, "round-1/build.md", "BUILD: READY")
        _, ticket = tickets.gate(ticket_id)
        self.assertEqual(
            tickets.round_results(ticket),
            [{"round": 1, "build": "READY", "gate": "FAIL", "review": None}, {"round": 2, "build": None, "gate": None, "review": None}],
        )


class SolutionTickets(FactoryCase):
    def test_a_solution_ticket_starts_in_research_with_the_parents_files(self):
        parent = self.open_ticket("Cut the cost", kind="research")
        tickets.update_ticket(parent, "Researching.", stage="research")
        self.put(parent, "solution.md", "RESEARCH: READY")
        tickets.record_levi(parent, "Which to build", "build A and B")
        child = tickets.create_ticket("Cut the cost: option A", None, str(self.target), parent=parent)
        self.assertEqual((child["stage"], child["kind"], child["parent"]), ("research", "research", parent))
        names = [f["path"] for f in tickets.list_files(child["id"])]
        self.assertEqual(names, ["request.md", "levi.md", "solution.md"])

    def test_the_parent_is_done_only_when_every_solution_ticket_is(self):
        parent = self.open_ticket("Cut the cost", kind="research")
        tickets.update_ticket(parent, "Researching.", stage="research")
        self.assertIn("solution tickets", self.refused(parent, "x", stage="done"))
        child = tickets.create_ticket("Cut the cost: option A", None, str(self.target), parent=parent)["id"]
        self.assertIn("solution tickets", self.refused(parent, "x", stage="done"))
        self.put(child, "plan.md", "PLAN: READY")
        tickets.update_ticket(child, "Planned.", stage="verification")
        self.put(child, "verification-plan.md", "VERIFICATION: READY")
        tickets.update_ticket(child, "Building.", stage="build")
        self.put(child, "round-1/build.md", "BUILD: READY")
        tickets.gate(child)
        self.put(child, "round-1/review.md", "REVIEW: ACCEPT")
        tickets.update_ticket(child, "Accepted.", stage="done")
        self.assertEqual(tickets.update_ticket(parent, "Levi picked A.", stage="done")["stage"], "done")


class WritersAtOnce(FactoryCase):
    def test_updates_from_two_processes_all_land(self):
        ticket_id = self.open_ticket()
        before = len(tickets.read_ticket(ticket_id)["updates"])
        script = "import tickets\nfor n in range(15): tickets.update_ticket(%r, 'note %%d' %% n)" % ticket_id
        writers = [subprocess.Popen([sys.executable, "-c", script], cwd=str(HERE)) for _ in range(2)]
        self.assertEqual([writer.wait() for writer in writers], [0, 0])
        self.assertEqual(len(tickets.read_ticket(ticket_id)["updates"]), before + 30)


class Usage(FactoryCase):
    def transcript(self, name, prompt, replies):
        folder = self.claude / "projects" / "-some-project" / "session-1" / "subagents"
        folder.mkdir(parents=True, exist_ok=True)
        lines = [{"type": "user", "timestamp": "2026-11-19T03:00:00Z", "message": {"content": prompt}}]
        for message_id, model, tokens in replies:
            lines.append({"type": "assistant", "timestamp": "2026-11-19T03:05:00Z", "message": {"id": message_id, "model": model, "usage": tokens}})
        (folder / ("agent-%s.jsonl" % name)).write_text("\n".join(json.dumps(line) for line in lines) + "\n")
        (folder / ("agent-%s.meta.json" % name)).write_text(json.dumps({"description": "Implementer round 1"}))

    def brief(self, ticket_id):
        return "Ticket folder: %s/\nRole: implementer." % tickets.ticket_folder(ticket_id)

    def test_cost_is_the_list_price_of_the_tokens(self):
        ticket_id = self.open_ticket()
        tokens = {"input_tokens": 1000000, "output_tokens": 1000000, "cache_read_input_tokens": 1000000,
                  "cache_creation_input_tokens": 2000000, "cache_creation": {"ephemeral_1h_input_tokens": 1000000}}
        self.transcript("a", self.brief(ticket_id), [("m1", "claude-opus-5-5", tokens)])
        found = usage.UsageIndex().by_ticket()[ticket_id]
        # opus 5.5: 4 in + 20 out + 0.2 cache read + 4 x 1.25 five-minute write + 4 x 2 one-hour write
        self.assertEqual(found["cost_usd"], 4 + 20 + 0.2 + 5 + 8)
        self.assertEqual(found["tokens"], 5000000)
        self.assertEqual(found["models"], ["claude-opus-5-5"])
        self.assertEqual(found["agents"][0]["label"], "Implementer round 1")

    def test_a_reply_written_as_several_lines_is_counted_once(self):
        ticket_id = self.open_ticket()
        partial, final = {"input_tokens": 10, "output_tokens": 1}, {"input_tokens": 10, "output_tokens": 500}
        self.transcript("a", self.brief(ticket_id), [("m1", "claude-opus-5-5", partial), ("m1", "claude-opus-5-5", final)])
        self.assertEqual(usage.UsageIndex().by_ticket()[ticket_id]["tokens"], 510)

    def test_a_model_with_no_listed_price_is_named_and_not_priced(self):
        ticket_id = self.open_ticket()
        self.transcript("a", self.brief(ticket_id), [("m1", "claude-unknown-9", {"input_tokens": 5, "output_tokens": 5})])
        found = usage.UsageIndex().by_ticket()[ticket_id]
        self.assertEqual((found["cost_usd"], found["unpriced"]), (0, ["claude-unknown-9"]))

    def test_a_transcript_without_the_ticket_line_is_not_counted(self):
        ticket_id = self.open_ticket()
        self.transcript("a", "Review this skill please.", [("m1", "claude-opus-5-5", {"input_tokens": 5, "output_tokens": 5})])
        self.assertNotIn(ticket_id, usage.UsageIndex().by_ticket())


if __name__ == "__main__":
    unittest.main()
