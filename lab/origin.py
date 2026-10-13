#!/usr/bin/env python3
"""Origin that folds HTTP method case so mixed-case DELETE is DELETE."""

from __future__ import annotations

import json
import os
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

WITNESS = os.environ.get("LAB_WITNESS", "ATS-IPALLOW-METHOD-CASE-WITNESS")
LISTEN_HOST = os.environ.get("ORIGIN_BIND", "0.0.0.0")
LISTEN_PORT = int(os.environ.get("ORIGIN_PORT", "8080"))

_lock = threading.Lock()
_hits: list[dict[str, str]] = []


class FoldingHandler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"
    server_version = "lab-origin/1.0"

    def log_message(self, fmt: str, *args: object) -> None:
        print(f"IOC origin {fmt % args}", flush=True)

    def handle_one_request(self) -> None:
        try:
            self.raw_requestline = self.rfile.readline(65537)
            if not self.raw_requestline:
                self.close_connection = True
                return
            if len(self.raw_requestline) > 65536:
                self.requestline = ""
                self.request_version = ""
                self.command = ""
                self.send_error(414)
                return
            if not self.parse_request():
                return
            original = self.command
            folded = original.upper()
            path = self.path.split("?", 1)[0]
            length = int(self.headers.get("Content-Length", "0") or "0")
            if length > 0:
                remaining = length
                while remaining > 0:
                    chunk = self.rfile.read(min(remaining, 8192))
                    if not chunk:
                        break
                    remaining -= len(chunk)
            with _lock:
                _hits.append({"original": original, "folded": folded, "path": path})
            print(
                f"IOC origin-hit original={original} folded={folded} path={path}",
                flush=True,
            )
            self._respond(original, folded, path)
        except (ConnectionResetError, BrokenPipeError, TimeoutError, OSError):
            self.close_connection = True

    def _respond(self, original: str, folded: str, path: str) -> None:
        if path in ("/hits", "/lab/hits"):
            with _lock:
                payload = json.dumps({"hits": list(_hits)}).encode("utf-8")
            self._send(200, payload, "application/json")
            return
        if folded == "DELETE":
            body = f"DELETED {WITNESS}\n".encode("utf-8")
            self._send(200, body, "text/plain")
            return
        if folded == "GET" and path in ("/", "/health"):
            self._send(200, b"GET-OK\n", "text/plain")
            return
        if folded == "GET":
            self._send(200, b"GET-OK\n", "text/plain")
            return
        if folded == "TRACE":
            body = f"TRACE-OK {WITNESS}\n".encode("utf-8")
            self._send(200, body, "text/plain")
            return
        if folded == "PURGE":
            self._send(200, b"PURGE-ORIGIN\n", "text/plain")
            return
        if folded == "PUSH":
            self._send(200, b"PUSH-ORIGIN\n", "text/plain")
            return
        self._send(200, f"{folded}-OK orig={original}\n".encode("utf-8"), "text/plain")

    def _send(self, code: int, body: bytes, content_type: str) -> None:
        self.close_connection = True
        self.send_response(code)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Connection", "close")
        self.end_headers()
        if body:
            self.wfile.write(body)


def main() -> int:
    httpd = ThreadingHTTPServer((LISTEN_HOST, LISTEN_PORT), FoldingHandler)
    print(f"IOC origin-listen {LISTEN_HOST}:{LISTEN_PORT} witness={WITNESS}", flush=True)
    httpd.serve_forever()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
