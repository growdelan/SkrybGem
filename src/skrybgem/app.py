"""Minimalna aplikacja webowa dla Milestone 0.5."""

from __future__ import annotations

import json
import os
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from importlib import resources

from .transcription import generate_final_text


def load_index_html() -> bytes:
    return resources.files("skrybgem.static").joinpath("index.html").read_bytes()


class AppHandler(BaseHTTPRequestHandler):
    server_version = "SkrybGem/0.1"

    def do_GET(self) -> None:
        if self.path != "/":
            self.send_error(HTTPStatus.NOT_FOUND)
            return

        body = load_index_html()
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self) -> None:
        if self.path != "/api/transcribe":
            self.send_error(HTTPStatus.NOT_FOUND)
            return

        content_length = int(self.headers.get("Content-Length", "0"))
        raw_body = self.rfile.read(content_length)

        try:
            payload = json.loads(raw_body.decode("utf-8"))
            audio_base64 = payload["audio_base64"]
            final_text = generate_final_text(audio_base64)
        except KeyError:
            self._send_json(
                HTTPStatus.BAD_REQUEST,
                {"error": "Brak pola audio_base64."},
            )
            return
        except (json.JSONDecodeError, UnicodeDecodeError):
            self._send_json(
                HTTPStatus.BAD_REQUEST,
                {"error": "Nieprawidłowy format żądania."},
            )
            return
        except ValueError as exc:
            self._send_json(
                HTTPStatus.UNPROCESSABLE_ENTITY,
                {"error": str(exc)},
            )
            return

        self._send_json(HTTPStatus.OK, {"text": final_text})

    def log_message(self, format: str, *args) -> None:
        return

    def _send_json(self, status: HTTPStatus, payload: dict[str, str]) -> None:
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def create_server(host: str = "127.0.0.1", port: int = 8000) -> ThreadingHTTPServer:
    return ThreadingHTTPServer((host, port), AppHandler)


def main() -> None:
    host = os.environ.get("SKRYBGEM_HOST", "127.0.0.1")
    port = int(os.environ.get("SKRYBGEM_PORT", "8000"))
    server = create_server(host, port)
    print(f"SkrybGem działa na http://{host}:{port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
