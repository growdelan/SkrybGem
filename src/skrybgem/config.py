"""Konfiguracja aplikacji ładowana z `.env` i środowiska."""

from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv


@dataclass(frozen=True)
class AppConfig:
    model_path: str
    host: str
    port: int


def load_app_config() -> AppConfig:
    load_dotenv()
    return AppConfig(
        model_path=os.environ.get("MODEL_PATH", "").strip(),
        host=os.environ.get("SKRYBGEM_HOST", "127.0.0.1").strip() or "127.0.0.1",
        port=int(os.environ.get("SKRYBGEM_PORT", "8000")),
    )
