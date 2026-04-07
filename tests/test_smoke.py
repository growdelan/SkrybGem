import json
import threading
import unittest
from http import HTTPStatus
from urllib import request

from skrybgem.app import create_server


class SmokeTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = create_server(port=0)
        cls.port = cls.server.server_address[1]
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join(timeout=2)

    def test_root_and_transcription_flow(self):
        response = request.urlopen(f"http://127.0.0.1:{self.port}/")
        html = response.read().decode("utf-8")
        self.assertEqual(response.status, HTTPStatus.OK)
        self.assertIn("Start nagrywania", html)
        self.assertIn("Finalny tekst", html)

        payload = json.dumps({"audio_base64": "AA" * 1024}).encode("utf-8")
        api_request = request.Request(
            f"http://127.0.0.1:{self.port}/api/transcribe",
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        api_response = request.urlopen(api_request)
        body = json.loads(api_response.read().decode("utf-8"))
        self.assertEqual(api_response.status, HTTPStatus.OK)
        self.assertEqual(body["text"], "To jest test.")
