"""Modello del dominio usato dal server MCP.

Le classi non dipendono dalla fonte dei dati: le usano sia l'impianto simulato
sia l'adattatore verso le KNX IoT 3rd Party API.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class AccessStatus:
    """Esito della verifica di accesso agli impianti dell'utente."""

    connected: bool
    detail: str


@dataclass(frozen=True)
class Installation:
    """Impianto domotico a cui l'utente ha accesso."""

    id: str
    name: str


@dataclass(frozen=True)
class Light:
    """Luce di un impianto, con l'ambiente in cui si trova."""

    id: str
    name: str
    room: str


@dataclass(frozen=True)
class LightState:
    """Stato di una luce in un certo momento."""

    id: str
    name: str
    room: str
    is_on: bool
