#!/usr/bin/env python3
"""Software factory: the command the orchestrator runs.

    new      open a ticket
    update   write an update, or move the ticket to another stage
    levi     save what Levi said, in his words
    red      before the first build, confirm the red checks fail
    gate     run the ticket's checks and move it on the result
    status   the ticket's stage and what every file in its folder says
    list     every ticket
    serve    run the live board

tickets.py holds the rules. usage.py reads cost. board.py serves the page.
"""

import argparse
import sys

import board
import tickets
from tickets import FactoryError
from usage import UsageIndex


def stdin_or(value):
    """`-` means the text is on stdin, so a long paste needs no shell quoting."""
    return sys.stdin.read() if value == "-" else value


def build_parser():
    parser = argparse.ArgumentParser(description="Software factory tickets, gate, and live board.")
    commands = parser.add_subparsers(dest="command", required=True)

    new = commands.add_parser("new", help="open a ticket")
    new.add_argument("--title", required=True, help="a few words that name the request")
    new.add_argument("--request", help="the request text, or - to read it from stdin")
    new.add_argument("--target", default="", help="path of the codebase the task changes")
    new.add_argument("--parent", help="the ticket whose solution this one builds; its request is reused")

    update = commands.add_parser("update", help="write one update to a ticket")
    update.add_argument("id")
    update.add_argument("--note", required=True, help="what just happened and what happens next")
    update.add_argument("--stage", choices=tickets.STAGES)
    update.add_argument("--state", choices=tickets.SETTABLE_STATES)
    update.add_argument("--kind", choices=tickets.KINDS)
    update.add_argument("--title", help="rename the ticket")
    update.add_argument("--target", help="set the codebase once it is known")
    update.add_argument("--more-rounds", action="store_true", help="Levi said to keep going past the round limit")

    levi = commands.add_parser("levi", help="save Levi's answer or decision in his words")
    levi.add_argument("id")
    levi.add_argument("--about", required=True, help="what he was answering, in a few words")
    levi.add_argument("words", help="his words, or - to read them from stdin")

    red = commands.add_parser("red", help="before the first build, run the red checks and confirm each one fails")
    red.add_argument("id")
    red.add_argument("--timeout", type=int, default=tickets.GATE_TIMEOUT_SECONDS, help="seconds before one red check is stopped")

    gate = commands.add_parser("gate", help="run the ticket's checks.sh and move the ticket on the result")
    gate.add_argument("id")
    gate.add_argument("--timeout", type=int, default=tickets.GATE_TIMEOUT_SECONDS, help="seconds before the checks are stopped")

    status = commands.add_parser("status", help="stage, round, and the first line and summary of every file")
    status.add_argument("id")

    commands.add_parser("list", help="list tickets")

    serve = commands.add_parser("serve", help="run the live board")
    serve.add_argument("--port", type=int, default=board.DEFAULT_PORT)
    return parser


def run_new(args):
    ticket = tickets.create_ticket(args.title, stdin_or(args.request) if args.request else None, args.target, args.parent)
    folder = tickets.ticket_folder(ticket["id"])
    print("Ticket: %s" % ticket["id"])
    print("Folder: %s" % folder)
    print("First line of every brief: Ticket folder: %s/" % folder)


def run_update(args):
    ticket = tickets.update_ticket(
        args.id, args.note, args.stage, args.state, args.kind, args.title, args.target, args.more_rounds
    )
    if ticket["stage"] == "done":
        tickets.save_usage(ticket["id"], UsageIndex().by_ticket().get(ticket["id"]))
    print("%s: %s, %s, round %d" % (ticket["id"], ticket["stage"], ticket["state"], ticket["rounds"]))


def run_red(args):
    verdict, ticket = tickets.red(args.id, args.timeout)
    print("RED: %s" % verdict)
    print("%s: %s, %s, round %d" % (ticket["id"], ticket["stage"], ticket["state"], ticket["rounds"]))


def run_gate(args):
    passed, ticket = tickets.gate(args.id, args.timeout)
    print("GATE: %s" % ("PASS" if passed else "FAIL"))
    print("%s: %s, %s, round %d" % (ticket["id"], ticket["stage"], ticket["state"], ticket["rounds"]))


def run_list():
    readable, unreadable = tickets.load_tickets()
    for ticket in readable:
        print("%s\t%s\t%s\t%s" % (ticket["id"], ticket["stage"], ticket["state"], ticket["title"]))
    for ticket_id in unreadable:
        print("%s\tunreadable" % ticket_id)


def run(args):
    if args.command == "new":
        run_new(args)
    elif args.command == "update":
        run_update(args)
    elif args.command == "levi":
        print("Saved: %s" % tickets.record_levi(args.id, args.about, stdin_or(args.words)))
    elif args.command == "red":
        run_red(args)
    elif args.command == "gate":
        run_gate(args)
    elif args.command == "status":
        print(tickets.status_text(args.id))
    elif args.command == "list":
        run_list()
    elif args.command == "serve":
        board.serve(args.port)


def main():
    args = build_parser().parse_args()
    try:
        run(args)
    except FactoryError as err:
        sys.exit("error: %s" % err)


if __name__ == "__main__":
    main()
