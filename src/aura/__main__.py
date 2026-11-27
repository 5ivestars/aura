"""Avvio del server MCP: `aura-server` oppure `python -m aura`."""

import logging

from aura.bootstrap import create_gateway
from aura.config import Settings
from aura.server import build_server


def main() -> None:
    """Legge la configurazione e avvia il server MCP su HTTP."""
    settings = Settings.from_env()
    logging.basicConfig(level=settings.log_level)
    logging.getLogger(__name__).info(
        "Avvio di AURA su %s:%d con backend '%s'", settings.host, settings.port, settings.backend
    )
    server = build_server(create_gateway(settings))
    server.run(transport="http", host=settings.host, port=settings.port, show_banner=False)


if __name__ == "__main__":
    main()
