"""Transkrypcja audio z użyciem LiteRT-LM."""

from __future__ import annotations

import base64
import binascii
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol


SYSTEM_PROMPT = (
    "Jesteś lokalnym modułem dyktowania dla aplikacji webowej. "
    "Użytkownik mówi po polsku, a Twoim zadaniem jest zwrócić wyłącznie "
    "finalny tekst po poprawieniu interpunkcji, wielkich liter i czytelności. "
    "Nie dodawaj żadnych komentarzy, wstępów, etykiet ani wyjaśnień. "
    "Nie zwracaj surowej transkrypcji. "
    "Zawsze użyj narzędzia return_final_text."
)

CONVERSATIONAL_PREFIX_RE = re.compile(
    r"^\s*(oto|poniżej|jasne|pewnie|oczywiście|transkrypcja|poprawiona transkrypcja)\b",
    re.IGNORECASE,
)


class TranscriptionError(Exception):
    """Bazowy błąd transkrypcji."""


class InvalidRequestError(TranscriptionError):
    """Nieprawidłowe wejście użytkownika."""


class ModelUnavailableError(TranscriptionError):
    """Model nie jest gotowy do użycia."""


class ProcessingError(TranscriptionError):
    """Nieoczekiwany błąd przetwarzania."""


class ModelClient(Protocol):
    def transcribe(self, audio_base64: str) -> str:
        """Zwraca finalny tekst dla payloadu audio zakodowanego jako base64."""

    def close(self) -> None:
        """Zamyka zasoby klienta modelowego."""


def decode_audio_payload(audio_base64: str) -> bytes:
    """Dekoduje payload audio przesłany z frontendu."""
    try:
        return base64.b64decode(audio_base64, validate=True)
    except (binascii.Error, ValueError, TypeError) as exc:
        raise InvalidRequestError("Nieprawidłowe dane audio.") from exc


def validate_wav_audio(audio_bytes: bytes) -> None:
    """Waliduje minimalny format wejścia audio."""
    if len(audio_bytes) < 256:
        raise InvalidRequestError("Nagranie jest puste albo zbyt krótkie.")
    if audio_bytes[:4] != b"RIFF" or audio_bytes[8:12] != b"WAVE":
        raise InvalidRequestError("Obsługiwane są tylko nagrania WAV z aplikacji.")


def normalize_final_text(text: str) -> str:
    """Porządkuje wynik modelu i odrzuca odpowiedzi konwersacyjne."""
    normalized = " ".join(text.strip().split())
    normalized = normalized.strip("\"' \n\t")
    if not normalized:
        raise ProcessingError("Model nie zwrócił finalnego tekstu.")
    if CONVERSATIONAL_PREFIX_RE.match(normalized):
        raise ProcessingError("Model zwrócił odpowiedź konwersacyjną zamiast finalnego tekstu.")
    if normalized[-1] not in ".!?":
        normalized += "."
    if normalized[0].isalpha():
        normalized = normalized[0].upper() + normalized[1:]
    return normalized


class LiteRTModelClient:
    """Prosta integracja z LiteRT-LM dla modelu audio."""

    def __init__(self, model_path: str):
        if not model_path:
            raise ModelUnavailableError("Brak zmiennej środowiskowej MODEL_PATH.")

        path = Path(model_path).expanduser()
        if not path.exists():
            raise ModelUnavailableError(f"Model nie istnieje pod ścieżką: {path}")

        try:
            import litert_lm
        except ImportError as exc:
            raise ModelUnavailableError("Brak zależności litert-lm w środowisku.") from exc

        self._litert_lm = litert_lm
        self._engine = None
        try:
            self._engine = litert_lm.Engine(
                str(path),
                backend=litert_lm.Backend.GPU,
                audio_backend=litert_lm.Backend.CPU,
            )
            self._engine.__enter__()
        except Exception as exc:  # pragma: no cover - zależne od natywnej biblioteki
            raise ModelUnavailableError(f"Nie udało się załadować modelu LiteRT-LM: {exc}") from exc

    def transcribe(self, audio_base64: str) -> str:
        if self._engine is None:
            raise ModelUnavailableError("Model nie został poprawnie zainicjalizowany.")

        tool_result: dict[str, str] = {}

        def return_final_text(final_text: str) -> str:
            tool_result["text"] = final_text
            return "OK"

        content = [
            {"type": "audio", "blob": audio_base64},
            {
                "type": "text",
                "text": (
                    "Przepisz tę wypowiedź po polsku i zwróć wyłącznie finalny tekst "
                    "po poprawieniu interpunkcji, wielkich liter i oczywistej czytelności."
                ),
            },
        ]

        try:
            with self._engine.create_conversation(
                messages=[{"role": "system", "content": SYSTEM_PROMPT}],
                tools=[return_final_text],
            ) as conversation:
                response = conversation.send_message({"role": "user", "content": content})
        except Exception as exc:  # pragma: no cover - zależne od natywnej biblioteki
            raise ProcessingError(f"LiteRT-LM nie przetworzył nagrania: {exc}") from exc

        if tool_result.get("text"):
            return tool_result["text"]

        try:
            return response["content"][0]["text"]
        except (KeyError, IndexError, TypeError) as exc:
            raise ProcessingError("Model nie zwrócił rozpoznawalnej odpowiedzi.") from exc

    def close(self) -> None:
        if self._engine is not None:
            self._engine.__exit__(None, None, None)
            self._engine = None


@dataclass
class TranscriptionService:
    """Serwis odpowiedzialny za walidację i wywołanie modelu."""

    client: ModelClient | None = None
    unavailable_reason: str | None = None

    def transcribe_audio(self, audio_base64: str) -> str:
        audio_bytes = decode_audio_payload(audio_base64)
        validate_wav_audio(audio_bytes)

        if self.client is None:
            raise ModelUnavailableError(self.unavailable_reason or "Model nie jest gotowy.")

        final_text = self.client.transcribe(audio_base64)
        return normalize_final_text(final_text)

    def close(self) -> None:
        if self.client is not None:
            self.client.close()


def build_transcription_service() -> TranscriptionService:
    model_path = os.environ.get("MODEL_PATH", "").strip()
    try:
        client = LiteRTModelClient(model_path)
    except ModelUnavailableError as exc:
        return TranscriptionService(client=None, unavailable_reason=str(exc))
    return TranscriptionService(client=client)
