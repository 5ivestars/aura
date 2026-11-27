import pytest

from aura.domain import Installation, Light, LightState
from aura.errors import AccessDeniedError, NotFoundError
from aura.fake_gateway import FakeGateway

pytestmark = pytest.mark.anyio


async def test_access_ok(gateway):
    status = await gateway.check_access()
    assert status.connected


async def test_lists_demo_installation(gateway):
    assert await gateway.list_installations() == [
        Installation(id="kit-demo", name="Kit View Wireless (simulato)")
    ]


async def test_lists_lights_with_rooms(gateway):
    lights = await gateway.list_lights("kit-demo")
    assert [light.room for light in lights] == ["Soggiorno", "Cucina", "Camera"]
    assert lights[0] == Light(id="luce-1", name="Luce soggiorno", room="Soggiorno")


async def test_light_state(gateway):
    state = await gateway.get_light_state("kit-demo", "luce-1")
    assert state == LightState(id="luce-1", name="Luce soggiorno", room="Soggiorno", is_on=True)
    assert not (await gateway.get_light_state("kit-demo", "luce-2")).is_on


async def test_unknown_installation(gateway):
    with pytest.raises(NotFoundError, match="non esiste"):
        await gateway.list_lights("altro")


async def test_unknown_light(gateway):
    with pytest.raises(NotFoundError, match="luce-9"):
        await gateway.get_light_state("kit-demo", "luce-9")


async def test_without_access():
    gateway = FakeGateway.with_demo_data(connected=False)
    assert not (await gateway.check_access()).connected
    with pytest.raises(AccessDeniedError):
        await gateway.list_installations()
    with pytest.raises(AccessDeniedError):
        await gateway.list_lights("kit-demo")
