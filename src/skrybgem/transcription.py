"""Minimalna logika bootstrapowa dla Milestone 0.5."""

from __future__ import annotations

import base64
import binascii


def decode_audio_payload(audio_base64: str) -> bytes:
    """Dekoduje payload audio przesłany z frontendu."""
    try:
        return base64.b64decode(audio_base64, validate=True)
    except (binascii.Error, ValueError) as exc:
        raise ValueError("Nieprawidłowe dane audio.") from exc


def transcribe_audio(audio_bytes: bytes) -> str:
    """Zwraca minimalny wynik transkrypcji dla niepustego nagrania."""
    if len(audio_bytes) < 1024:
        raise ValueError("Nagranie jest puste albo zbyt krótkie.")
    return "to jest test"


def normalize_text(text: str) -> str:
    """Nadaje podstawową formę pisemną wynikowi bootstrapowemu."""
    normalized = " ".join(text.strip().split())
    if not normalized:
        raise ValueError("Brak tekstu do poprawienia.")
    normalized = normalized[0].upper() + normalized[1:]
    if normalized[-1] not in ".!?":
        normalized += "."
    return normalized


def generate_final_text(audio_base64: str) -> str:
    """Pełna minimalna ścieżka przetwarzania dla Milestone 0.5."""
    audio_bytes = decode_audio_payload(audio_base64)
    transcript = transcribe_audio(audio_bytes)
    return normalize_text(transcript)
