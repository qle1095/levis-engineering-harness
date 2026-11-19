"""Usage: each ticket's model, tokens, and cost, read from Claude Code's sub-agent transcripts.

Claude Code writes each sub-agent's messages, with the model and token counts, to
<config>/projects/<project>/<session>/subagents/agent-<id>.jsonl. That layout is not a
documented interface. If it changes, the board shows no usage; nothing else depends on it.
"""

import json
import os
import re
import threading
import time
from pathlib import Path

from tickets import TICKET_ID, FactoryError

PRICES_FILE = Path(__file__).with_name("prices.json")
# A brief that starts with this line ties the sub-agent's transcript to its ticket.
BRIEF_LINE = re.compile(r"Ticket folder: (\S+)")
TOKEN_KINDS = ("input", "output", "cache_read", "cache_write_5m", "cache_write_1h")


def transcripts():
    config = os.environ.get("CLAUDE_CONFIG_DIR")
    projects = (Path(config) if config else Path.home() / ".claude") / "projects"
    return projects.glob("*/*/subagents/agent-*.jsonl")


def load_prices():
    try:
        return json.loads(PRICES_FILE.read_text(encoding="utf-8"))
    except (OSError, ValueError) as err:
        raise FactoryError("cannot read the price list %s: %s" % (PRICES_FILE, err))


def price_for(model, prices):
    """The listed price for a model id. Ids can carry a suffix, so the listed name is matched as a prefix."""
    for name, price in prices["models"].items():
        if model.startswith(name):
            return price
    return None


def cost_usd(tokens, price, prices):
    per_million = (
        tokens["input"] * price["input"]
        + tokens["output"] * price["output"]
        + tokens["cache_read"] * price["cache_read"]
        + tokens["cache_write_5m"] * price["input"] * prices["cache_write_5m_multiplier"]
        + tokens["cache_write_1h"] * price["input"] * prices["cache_write_1h_multiplier"]
    )
    return per_million / 1e6


def message_tokens(usage):
    written = usage.get("cache_creation_input_tokens", 0)
    written_1h = (usage.get("cache_creation") or {}).get("ephemeral_1h_input_tokens", 0)
    return {
        "input": usage.get("input_tokens", 0),
        "output": usage.get("output_tokens", 0),
        "cache_read": usage.get("cache_read_input_tokens", 0),
        "cache_write_5m": written - written_1h,
        "cache_write_1h": written_1h,
    }


def prompt_text(entry):
    content = (entry.get("message") or {}).get("content", "")
    if isinstance(content, str):
        return content
    return " ".join(block.get("text", "") for block in content if isinstance(block, dict))


def ticket_named_in(path):
    """The ticket id on the brief's first line, or None when this transcript is not a factory brief."""
    with path.open(encoding="utf-8") as lines:
        first = lines.readline()
    try:
        named = BRIEF_LINE.match(prompt_text(json.loads(first)).lstrip())
    except ValueError:
        return None
    folder = Path(named.group(1).rstrip("/.")) if named else None
    if folder is None or folder.parent.name != "tickets" or not TICKET_ID.match(folder.name):
        return None
    return folder.name


def agent_label(path):
    """What the orchestrator called this sub-agent when it spawned it."""
    try:
        meta = json.loads(path.with_name(path.name.replace(".jsonl", ".meta.json")).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return path.stem
    return meta.get("description") or meta.get("agentType") or path.stem


def read_agent(path, prices):
    """One sub-agent's model, tokens, cost, and times."""
    by_message, started, ended = {}, None, None
    with path.open(encoding="utf-8") as lines:
        for line in lines:
            try:
                entry = json.loads(line)
            except ValueError:
                continue  # the last line of a running agent can be half written
            ended = entry.get("timestamp") or ended
            started = started or ended
            message = entry.get("message")
            if entry.get("type") == "assistant" and isinstance(message, dict) and message.get("usage"):
                # One reply is written as several lines with the same id. The last one has the final counts.
                by_message[message.get("id")] = (message.get("model") or "unknown", message["usage"])

    tokens = dict.fromkeys(TOKEN_KINDS, 0)
    output_by_model, cost, unpriced = {}, 0.0, set()
    for model, usage in by_message.values():
        spent = message_tokens(usage)
        for kind in TOKEN_KINDS:
            tokens[kind] += spent[kind]
        output_by_model[model] = output_by_model.get(model, 0) + spent["output"]
        price = price_for(model, prices)
        if price is None:
            unpriced.add(model)
        else:
            cost += cost_usd(spent, price, prices)
    return {
        "label": agent_label(path),
        "model": max(output_by_model, key=output_by_model.get) if output_by_model else None,
        "tokens": tokens,
        "cost_usd": round(cost, 4),
        "unpriced": sorted(unpriced),
        "started": started,
        "ended": ended,
    }


class UsageIndex:
    """Each ticket's sub-agents. Reads a transcript again only when the file changed."""

    def __init__(self):
        self.files = {}  # path -> {"ticket": id or None, "stamp": (mtime, size), "agent": {...}}
        self.scanned_at = 0.0
        self.lock = threading.Lock()

    def scan(self):
        prices = load_prices()
        for path in transcripts():
            known = self.files.get(path)
            if known is None:
                # A prompt never changes, so each transcript is matched to a ticket once.
                known = self.files[path] = {"ticket": ticket_named_in(path), "stamp": None, "agent": None}
            if known["ticket"] is None:
                continue
            stat = path.stat()
            stamp = (stat.st_mtime, stat.st_size)
            if stamp != known["stamp"]:
                known["agent"], known["stamp"] = read_agent(path, prices), stamp

    def by_ticket(self, max_age=0):
        with self.lock:
            if time.time() - self.scanned_at >= max_age:
                self.scan()
                self.scanned_at = time.time()
            grouped = {}
            for known in self.files.values():
                if known["agent"]:
                    grouped.setdefault(known["ticket"], []).append(known["agent"])
        return {ticket: summarize_usage(agents) for ticket, agents in grouped.items()}


def summarize_usage(agents):
    agents = sorted(agents, key=lambda agent: agent["started"] or "")
    return {
        "cost_usd": round(sum(agent["cost_usd"] for agent in agents), 2),
        "tokens": sum(sum(agent["tokens"].values()) for agent in agents),
        "models": sorted({agent["model"] for agent in agents if agent["model"]}),
        "unpriced": sorted({model for agent in agents for model in agent["unpriced"]}),
        "agents": agents,
    }
