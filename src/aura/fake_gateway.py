"""Impianto simulato in memoria, per lo sviluppo e per i test automatici.

I dati di esempio riprendono le luci del kit descritto nel capitolato
(tre attuatori per il controllo delle luci); nomi e identificativi sono inventati.
"""

from dataclasses import dataclass, field

from aura.domain import AccessStatus, Installation, Light, LightState
from aura.errors import AccessDeniedError, NotFoundError


@dataclass
class _FakeLight:
    light: Light
    is_on: bool


@dataclass
class _FakeInstallation:
    installation: Installation
    lights: dict[str, _FakeLight] = field(default_factory=dict)


class FakeGateway:
    """Implementazione di `InstallationGateway` che tiene i dati in memoria."""

    def __init__(self, installations: list[_FakeInstallation], *, connected: bool = True) -> None:
        self._installations = {item.installation.id: item for item in installations}
        self._connected = connected

    @classmethod
    def with_demo_data(cls, *, connected: bool = True) -> FakeGateway:
        """Crea un impianto simulato con tre luci in tre ambienti."""
        demo = _FakeInstallation(Installation(id="kit-demo", name="Kit View Wireless (simulato)"))
        for light_id, name, room, is_on in (
            ("luce-1", "Luce soggiorno", "Soggiorno", True),
            ("luce-2", "Luce cucina", "Cucina", False),
            ("luce-3", "Luce camera", "Camera", False),
        ):
            demo.lights[light_id] = _FakeLight(Light(id=light_id, name=name, room=room), is_on)
        return cls([demo], connected=connected)

    async def check_access(self) -> AccessStatus:
        if not self._connected:
            return AccessStatus(connected=False, detail="Impianto simulato non raggiungibile.")
        return AccessStatus(connected=True, detail="Impianto simulato raggiungibile.")

    async def list_installations(self) -> list[Installation]:
        self._ensure_connected()
        return [item.installation for item in self._installations.values()]

    async def list_lights(self, installation_id: str) -> list[Light]:
        installation = self._get_installation(installation_id)
        return [item.light for item in installation.lights.values()]

    async def get_light_state(self, installation_id: str, light_id: str) -> LightState:
        installation = self._get_installation(installation_id)
        item = installation.lights.get(light_id)
        if item is None:
            raise NotFoundError(
                f"La luce '{light_id}' non esiste nell'impianto '{installation_id}'."
            )
        light = item.light
        return LightState(id=light.id, name=light.name, room=light.room, is_on=item.is_on)

    def _ensure_connected(self) -> None:
        if not self._connected:
            raise AccessDeniedError("Accesso agli impianti non disponibile.")

    def _get_installation(self, installation_id: str) -> _FakeInstallation:
        self._ensure_connected()
        installation = self._installations.get(installation_id)
        if installation is None:
            raise NotFoundError(f"L'impianto '{installation_id}' non esiste.")
        return installation
