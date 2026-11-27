"""Adattatore verso le KNX IoT 3rd Party API (v2.1.0), con autenticazione OAuth2.

Da implementare seguendo la documentazione per integratori di Vimar.
Quella documentazione e le credenziali sono riservate: non vanno copiate
nei commenti, nelle issue o in strumenti esterni. I valori di accesso
arrivano solo dalle variabili d'ambiente (file config.env, escluso da git).
"""

from aura.config import Settings
from aura.domain import AccessStatus, Installation, Light, LightState

_NOT_IMPLEMENTED = "Adattatore KNX IoT non ancora implementato: usare AURA_BACKEND=fake."


class KnxIotGateway:
    """Implementazione di `InstallationGateway` per l'impianto reale (da completare)."""

    def __init__(self, settings: Settings) -> None:
        self._settings = settings

    async def check_access(self) -> AccessStatus:
        raise NotImplementedError(_NOT_IMPLEMENTED)

    async def list_installations(self) -> list[Installation]:
        raise NotImplementedError(_NOT_IMPLEMENTED)

    async def list_lights(self, installation_id: str) -> list[Light]:
        raise NotImplementedError(_NOT_IMPLEMENTED)

    async def get_light_state(self, installation_id: str, light_id: str) -> LightState:
        raise NotImplementedError(_NOT_IMPLEMENTED)
