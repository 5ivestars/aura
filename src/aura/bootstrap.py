"""Collegamento dei componenti: sceglie l'implementazione dell'impianto dalla configurazione."""

from aura.config import Settings
from aura.fake_gateway import FakeGateway
from aura.gateway import InstallationGateway
from aura.knx_gateway import KnxIotGateway


def create_gateway(settings: Settings) -> InstallationGateway:
    """Restituisce l'implementazione indicata da `AURA_BACKEND`."""
    if settings.backend == "knx":
        return KnxIotGateway(settings)
    return FakeGateway.with_demo_data()
