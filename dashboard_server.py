"""Shepherd Dashboard Server — localhost:8384"""

import json
import tempfile
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path

SHEPHERD_DIR = Path(__file__).parent
LOG_FILE = SHEPHERD_DIR / "shepherd_log.jsonl"
PLAN_FILE = SHEPHERD_DIR / "PLAN.md"
HTML_FILE = SHEPHERD_DIR / "dashboard.html"
TMP_DIR = Path(tempfile.gettempdir()) / "shepherd"


def read_log_all() -> list[dict]:
    if not LOG_FILE.exists():
        return []
    entries = []
    for line in LOG_FILE.read_text(encoding="utf-8").strip().splitlines():
        try:
            entries.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return entries


def read_log(limit: int = 100) -> list[dict]:
    if not LOG_FILE.exists():
        return []
    lines = LOG_FILE.read_text(encoding="utf-8").strip().splitlines()
    entries = []
    for line in lines[-limit:]:
        try:
            entries.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return entries


def parse_plan() -> dict:
    if not PLAN_FILE.exists():
        return {"raw": "", "goal": "", "phase": ""}
    text = PLAN_FILE.read_text(encoding="utf-8")
    goal = ""
    phase = ""
    in_goal = False
    in_phase = False
    for line in text.splitlines():
        if line.startswith("## Goal"):
            in_goal = True
            in_phase = False
            continue
        if line.startswith("## Current Phase"):
            in_phase = True
            in_goal = False
            continue
        if line.startswith("## "):
            in_goal = False
            in_phase = False
            continue
        if in_goal and line.strip():
            goal += line.strip() + " "
        if in_phase and line.strip() and not line.strip().startswith("<!--"):
            phase += line.strip() + " "
    return {"goal": goal.strip(), "phase": phase.strip(), "raw": text}


def read_status() -> dict:
    status = {"chunk_count": 0, "cliff_warning": None, "active": False}
    count_file = TMP_DIR / "chunk_count"
    if count_file.exists():
        try:
            status["chunk_count"] = int(count_file.read_text().strip())
        except (ValueError, OSError):
            pass
    cliff_file = TMP_DIR / "cliff_warning.json"
    if cliff_file.exists():
        try:
            status["cliff_warning"] = json.loads(cliff_file.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            pass
    active_file = Path(tempfile.gettempdir()) / "shepherd-active"
    status["active"] = active_file.exists()
    return status


class Handler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self._serve_html()
        elif self.path == "/api/log":
            self._json_response(read_log())
        elif self.path == "/api/log/all":
            self._json_response(read_log_all())
        elif self.path == "/api/plan":
            self._json_response(parse_plan())
        elif self.path == "/api/status":
            self._json_response(read_status())
        else:
            self.send_error(404)

    def _json_response(self, data):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Length", len(body))
        self.end_headers()
        self.wfile.write(body)

    def _serve_html(self):
        if not HTML_FILE.exists():
            self.send_error(404, "dashboard.html not found")
            return
        body = HTML_FILE.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", len(body))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        pass  # quiet


def main():
    import sys
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8385
    server = HTTPServer(("127.0.0.1", port), Handler)
    server.allow_reuse_address = True
    print(f"Shepherd Dashboard: http://localhost:{port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutdown.")
        server.server_close()


if __name__ == "__main__":
    main()
