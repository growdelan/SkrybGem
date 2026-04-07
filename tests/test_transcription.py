import base64
import unittest

from skrybgem.transcription import (
    InvalidRequestError,
    ModelUnavailableError,
    ProcessingError,
    TranscriptionService,
    decode_audio_payload,
    normalize_final_text,
)


class FakeClient:
    def __init__(self, result=None, error=None):
        self.result = result
        self.error = error
        self.closed = False

    def transcribe(self, audio_base64: str) -> str:
        if self.error is not None:
            raise self.error
        return self.result

    def close(self) -> None:
        self.closed = True


def build_wav_base64(frame_count: int = 2048) -> str:
    data_size = frame_count * 2
    header = bytearray()
    header.extend(b"RIFF")
    header.extend((36 + data_size).to_bytes(4, "little"))
    header.extend(b"WAVE")
    header.extend(b"fmt ")
    header.extend((16).to_bytes(4, "little"))
    header.extend((1).to_bytes(2, "little"))
    header.extend((1).to_bytes(2, "little"))
    header.extend((16000).to_bytes(4, "little"))
    header.extend((32000).to_bytes(4, "little"))
    header.extend((2).to_bytes(2, "little"))
    header.extend((16).to_bytes(2, "little"))
    header.extend(b"data")
    header.extend(data_size.to_bytes(4, "little"))
    header.extend(b"\x00" * data_size)
    return base64.b64encode(bytes(header)).decode("ascii")


class TranscriptionServiceTest(unittest.TestCase):
    def test_decode_audio_payload_rejects_invalid_base64(self):
        with self.assertRaises(InvalidRequestError):
            decode_audio_payload("!!!")

    def test_service_returns_normalized_text(self):
        service = TranscriptionService(client=FakeClient(result="to jest test"))
        result = service.transcribe_audio(build_wav_base64())
        self.assertEqual(result, "To jest test.")

    def test_service_rejects_empty_audio(self):
        service = TranscriptionService(client=FakeClient(result="to jest test"))
        with self.assertRaises(InvalidRequestError):
            service.transcribe_audio(build_wav_base64(frame_count=8))

    def test_service_rejects_non_wav_audio(self):
        invalid_audio = base64.b64encode(b"not-wav-at-all" * 32).decode("ascii")
        service = TranscriptionService(client=FakeClient(result="to jest test"))
        with self.assertRaises(InvalidRequestError):
            service.transcribe_audio(invalid_audio)

    def test_service_reports_model_unavailable(self):
        service = TranscriptionService(client=None, unavailable_reason="Brak modelu.")
        with self.assertRaises(ModelUnavailableError):
            service.transcribe_audio(build_wav_base64())

    def test_service_propagates_processing_error(self):
        service = TranscriptionService(client=FakeClient(error=ProcessingError("awaria")))
        with self.assertRaises(ProcessingError):
            service.transcribe_audio(build_wav_base64())

    def test_service_closes_client(self):
        client = FakeClient(result="to jest test")
        service = TranscriptionService(client=client)
        service.close()
        self.assertTrue(client.closed)


class NormalizeFinalTextTest(unittest.TestCase):
    def test_strips_textual_tool_wrapper(self):
        self.assertEqual(
            normalize_final_text(
                "Return_final_text{final_text: To jest nagrywanie głosu mojej nowej aplikacji. Chciałbym zobaczyć, jak to działa. Dziękuję. }."
            ),
            "To jest nagrywanie głosu mojej nowej aplikacji. Chciałbym zobaczyć, jak to działa. Dziękuję.",
        )

    def test_strips_litert_control_tokens(self):
        self.assertEqual(
            normalize_final_text('<|"|>To jest moje nagrywanie, chciałbym tylko tyle powiedzieć.<|"|>'),
            "To jest moje nagrywanie, chciałbym tylko tyle powiedzieć.",
        )

    def test_rejects_conversational_prefix(self):
        with self.assertRaises(ProcessingError):
            normalize_final_text("Oto poprawiona transkrypcja: To jest test.")

    def test_rejects_empty_text(self):
        with self.assertRaises(ProcessingError):
            normalize_final_text("   ")
