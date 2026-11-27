"""Interfaccia verso l'impianto domotico.

Il server MCP dipende solo da questa interfaccia e riceve l'implementazione
dall'esterno (dependency injection): l'impianto simulato per sviluppo e test,
l'adattatore KNX IoT per l'impianto reale. Si passa dall'una all'altra
cambiando solo la configurazione.
"""

from typing import Protocol

from aura.domain import AccessStatus, Installation, Light, LightState


class InstallationGateway(Protocol):
    """Operazioni sull'impianto usate dagli strumenti MCP.

    Le implementazioni segnalano i problemi con le eccezioni di `aura.errors`.
    """

    async def check_access(self) -> AccessStatus:
        """Verifica se l'accesso agli impianti dell'utente funziona."""
        ...

    async def list_installations(self) -> list[Installation]:
        """Restituisce gli impianti a cui l'utente ha accesso."""
        ...

    async def list_lights(self, installation_id: str) -> list[Light]:
        """Restituisce le luci di un impianto."""
        ...

    async def get_light_state(self, installation_id: str, light_id: str) -> LightState:
        """Restituisce lo stato attuale di una luce."""
        ...
