import json
import os
import threading
import unittest
from http import HTTPStatus
from unittest import mock
from urllib import error, request

from skrybgem.app import create_server
from skrybgem.transcription import InvalidRequestError, ModelUnavailableError, ProcessingError
from tests.test_transcription import build_wav_base64


class FakeService:
    def __init__(self, result="To jest test.", error_to_raise=None):
        self.result = result
        self.error_to_raise = error_to_raise
        self.closed = False

    def transcribe_audio(self, audio_base64: str) -> str:
        if self.error_to_raise:
            raise self.error_to_raise
        return self.result

    def close(self) -> None:
        self.closed = True


class AppTest(unittest.TestCase):
    def setUp(self):
        self.fake_service = FakeService()
        self.server = create_server(port=0, transcription_service=self.fake_service)
        self.port = self.server.server_address[1]
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(timeout=2)

    def post_json(self, payload, raw=False):
        data = payload if raw else json.dumps(payload).encode("utf-8")
        api_request = request.Request(
            f"http://127.0.0.1:{self.port}/api/transcribe",
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            return request.urlopen(api_request)
        except error.HTTPError as exc:
            return exc

    def test_root_renders_interface(self):
        response = request.urlopen(f"http://127.0.0.1:{self.port}/")
        html = response.read().decode("utf-8")
        self.assertEqual(response.status, HTTPStatus.OK)
        self.assertIn("SkrybGem", html)
        self.assertIn("Start nagrywania", html)
        self.assertIn("Nagrywanie...", html)
        self.assertIn("Przetwarzanie...", html)
        self.assertIn("Kopiuj tekst", html)
        self.assertIn("Finalny tekst", html)

    def test_transcription_success(self):
        response = self.post_json({"audio_base64": "AAAA"})
        body = json.loads(response.read().decode("utf-8"))
        self.assertEqual(response.status, HTTPStatus.OK)
        self.assertEqual(body["text"], "To jest test.")

    def test_missing_audio_field_returns_400(self):
        response = self.post_json({})
        body = json.loads(response.read().decode("utf-8"))
        self.assertEqual(response.status, HTTPStatus.BAD_REQUEST)
        self.assertIn("audio_base64", body["error"])

    def test_invalid_json_returns_400(self):
        response = self.post_json(b"{not-json", raw=True)
        body = json.loads(response.read().decode("utf-8"))
        self.assertEqual(response.status, HTTPStatus.BAD_REQUEST)
        self.assertIn("format", body["error"].lower())

    def test_invalid_request_returns_422(self):
        self.fake_service.error_to_raise = InvalidRequestError("Nagranie jest puste.")
        response = self.post_json({"audio_base64": "AAAA"})
        body = json.loads(response.read().decode("utf-8"))
        self.assertEqual(response.status, HTTPStatus.UNPROCESSABLE_ENTITY)
        self.assertIn("puste", body["error"])

    def test_model_unavailable_returns_503(self):
        self.fake_service.error_to_raise = ModelUnavailableError("Brak modelu.")
        response = self.post_json({"audio_base64": "AAAA"})
        body = json.loads(response.read().decode("utf-8"))
        self.assertEqual(response.status, HTTPStatus.SERVICE_UNAVAILABLE)
        self.assertIn("modelu", body["error"].lower())

    def test_default_service_returns_503_when_model_path_is_missing(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(timeout=2)

        with mock.patch.dict(os.environ, {"MODEL_PATH": ""}):
            self.server = create_server(port=0)
            self.port = self.server.server_address[1]
            self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
            self.thread.start()

        response = self.post_json({"audio_base64": build_wav_base64()})
        body = json.loads(response.read().decode("utf-8"))
        self.assertEqual(response.status, HTTPStatus.SERVICE_UNAVAILABLE)
        self.assertIn("model_path", body["error"].lower())

    def test_processing_error_returns_500(self):
        self.fake_service.error_to_raise = ProcessingError("Awaria przetwarzania.")
        response = self.post_json({"audio_base64": "AAAA"})
        body = json.loads(response.read().decode("utf-8"))
        self.assertEqual(response.status, HTTPStatus.INTERNAL_SERVER_ERROR)
        self.assertIn("awaria", body["error"].lower())

    def test_server_closes_service(self):
        self.server.server_close()
        self.assertTrue(self.fake_service.closed)
