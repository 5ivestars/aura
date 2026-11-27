"""Configurazione letta dalle variabili d'ambiente (vedi config.env.example)."""

import os
from collections.abc import Mapping
from dataclasses import dataclass

from aura.errors import ConfigError

BACKENDS = ("fake", "knx")
LOG_LEVELS = ("DEBUG", "INFO", "WARNING", "ERROR")


@dataclass(frozen=True)
class Settings:
    """Parametri di avvio del server MCP."""

    backend: str = "fake"
    host: str = "127.0.0.1"
    port: int = 8000
    log_level: str = "INFO"

    @classmethod
    def from_env(cls, env: Mapping[str, str] | None = None) -> Settings:
        """Legge la configurazione; le variabili mancanti prendono il valore predefinito."""
        env = os.environ if env is None else env

        backend = env.get("AURA_BACKEND", cls.backend).strip().lower()
        if backend not in BACKENDS:
            raise ConfigError(f"AURA_BACKEND deve valere {' o '.join(BACKENDS)}, non '{backend}'.")

        log_level = env.get("AURA_LOG_LEVEL", cls.log_level).strip().upper()
        if log_level not in LOG_LEVELS:
            raise ConfigError(f"AURA_LOG_LEVEL deve essere uno tra {', '.join(LOG_LEVELS)}.")

        raw_port = env.get("AURA_PORT", str(cls.port)).strip()
        try:
            port = int(raw_port)
        except ValueError:
            raise ConfigError(f"AURA_PORT deve essere un numero, non '{raw_port}'.") from None
        if not 1 <= port <= 65535:
            raise ConfigError(f"AURA_PORT deve essere tra 1 e 65535, non {port}.")

        host = env.get("AURA_HOST", cls.host).strip() or cls.host
        return cls(backend=backend, host=host, port=port, log_level=log_level)
