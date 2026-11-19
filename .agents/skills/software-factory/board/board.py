"""The live board: a local page that shows every ticket, and the small API it reads.

The board only reads. It never changes a ticket.
"""

import errno
import json
import urllib.error
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import tickets
from tickets import FactoryError
from usage import UsageIndex

DEFAULT_PORT = 4747
BOARD_PAGE = Path(__file__).with_name("board.html")
# How often the running board looks for new sub-agent transcripts.
USAGE_SCAN_SECONDS = 10
# The list leaves these out. They can be long, and the list is asked for every two seconds.
DETAIL_ONLY_FIELDS = ("updates",)

LIVE_USAGE = UsageIndex()


def with_usage(ticket):
    """A done ticket carries its own totals. A ticket on the line is read from the transcripts."""
    if not ticket.get("usage"):
        ticket["usage"] = LIVE_USAGE.by_ticket(max_age=USAGE_SCAN_SECONDS).get(ticket["id"])
    return ticket


def summarize(ticket):
    summary = {key: value for key, value in with_usage(ticket).items() if key not in DETAIL_ONLY_FIELDS}
    summary["last_note"] = ticket["updates"][-1]["note"] if ticket["updates"] else ""
    summary["round_results"] = tickets.round_results(ticket)
    if summary["usage"]:
        # The per-agent rows are for the drawer.
        summary["usage"] = {key: value for key, value in summary["usage"].items() if key != "agents"}
    return summary


def board_payload():
    readable, unreadable = tickets.load_tickets()
    return {
        "home": str(tickets.factory_home()),
        "tickets": [summarize(ticket) for ticket in readable],
        "unreadable": unreadable,
    }


def ticket_payload(ticket_id):
    ticket = with_usage(tickets.read_ticket(ticket_id))
    ticket["round_results"] = tickets.round_results(ticket)
    ticket["files"] = tickets.list_files(ticket_id)
    return ticket


class BoardHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if not self.host_is_local():
            # A page on another site can point its own name at 127.0.0.1 to read the tickets.
            self.respond(403, "text/plain; charset=utf-8", b"this board only answers on localhost")
            return
        route = self.path.split("?", 1)[0]
        if route == "/":
            self.respond(200, "text/html; charset=utf-8", BOARD_PAGE.read_bytes())
        elif route == "/api/tickets":
            self.respond_json(board_payload())
        elif route.startswith("/api/tickets/"):
            self.respond_ticket_route(route[len("/api/tickets/"):])
        else:
            self.respond(404, "text/plain; charset=utf-8", b"not found")

    def host_is_local(self):
        port = self.server.server_address[1]
        return self.headers.get("Host") in ("127.0.0.1:%d" % port, "localhost:%d" % port)

    def respond_ticket_route(self, rest):
        """`<id>` is the full ticket. `<id>/files/<path>` is one document from its folder."""
        ticket_id, _, document = rest.partition("/files/")
        try:
            if document:
                text = tickets.read_file(ticket_id, document)
                self.respond(200, "text/plain; charset=utf-8", text.encode("utf-8"))
            else:
                self.respond_json(ticket_payload(ticket_id))
        except FactoryError as err:
            self.respond(404, "text/plain; charset=utf-8", str(err).encode("utf-8"))

    def respond_json(self, payload):
        self.respond(200, "application/json", json.dumps(payload).encode("utf-8"))

    def respond(self, status, content_type, body):
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        # An open board asks every two seconds. Logging each ask is noise.
        pass


def board_is_running(url):
    try:
        with urllib.request.urlopen(url + "/api/tickets", timeout=2) as response:
            return "tickets" in json.loads(response.read().decode("utf-8"))
    except (urllib.error.URLError, OSError, ValueError):
        return False


def serve(port):
    url = "http://127.0.0.1:%d" % port
    try:
        # Loopback only. Tickets hold request text and are not for the network.
        server = ThreadingHTTPServer(("127.0.0.1", port), BoardHandler)
    except OSError as err:
        if err.errno != errno.EADDRINUSE:
            raise FactoryError("cannot start the board on port %d: %s" % (port, err))
        if board_is_running(url):
            print("Board already running at %s" % url)
            return
        raise FactoryError("port %d is used by something that is not the board. Pass --port." % port)
    print("Board running at %s" % url, flush=True)
    print("Tickets: %s" % tickets.tickets_dir(), flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
