"""Aplikacja webowa SkrybGem."""

from __future__ import annotations

import json
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from importlib import resources

from .config import load_app_config
from .transcription import (
    InvalidRequestError,
    ModelUnavailableError,
    ProcessingError,
    TranscriptionService,
    build_transcription_service,
)


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
            final_text = self.server.transcription_service.transcribe_audio(audio_base64)
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
        except InvalidRequestError as exc:
            self._send_json(
                HTTPStatus.UNPROCESSABLE_ENTITY,
                {"error": str(exc)},
            )
            return
        except ModelUnavailableError as exc:
            self._send_json(
                HTTPStatus.SERVICE_UNAVAILABLE,
                {"error": str(exc)},
            )
            return
        except ProcessingError as exc:
            self._send_json(
                HTTPStatus.INTERNAL_SERVER_ERROR,
                {"error": str(exc)},
            )
            return
        except Exception:
            self._send_json(
                HTTPStatus.INTERNAL_SERVER_ERROR,
                {"error": "Wystąpił nieoczekiwany błąd przetwarzania."},
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


class SkrybGemServer(ThreadingHTTPServer):
    def __init__(
        self,
        server_address: tuple[str, int],
        handler_cls: type[BaseHTTPRequestHandler],
        transcription_service: TranscriptionService,
    ):
        self.transcription_service = transcription_service
        super().__init__(server_address, handler_cls)

    def server_close(self) -> None:
        self.transcription_service.close()
        super().server_close()


def create_server(
    host: str = "127.0.0.1",
    port: int = 8000,
    transcription_service: TranscriptionService | None = None,
) -> SkrybGemServer:
    service = transcription_service or build_transcription_service()
    return SkrybGemServer((host, port), AppHandler, service)


def main() -> None:
    config = load_app_config()
    server = create_server(config.host, config.port)
    print(f"SkrybGem działa na http://{config.host}:{config.port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
