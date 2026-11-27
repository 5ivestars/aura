import pytest

import aura.__main__ as entrypoint
from aura.bootstrap import create_gateway
from aura.config import Settings
from aura.fake_gateway import FakeGateway
from aura.knx_gateway import KnxIotGateway


def test_fake_backend_by_default():
    assert isinstance(create_gateway(Settings()), FakeGateway)


def test_knx_backend():
    assert isinstance(create_gateway(Settings(backend="knx")), KnxIotGateway)


@pytest.mark.anyio
async def test_knx_gateway_is_not_implemented_yet():
    gateway = KnxIotGateway(Settings(backend="knx"))
    for call in (
        gateway.check_access(),
        gateway.list_installations(),
        gateway.list_lights("x"),
        gateway.get_light_state("x", "y"),
    ):
        with pytest.raises(NotImplementedError):
            await call


def test_main_starts_http_server(monkeypatch):
    calls = {}

    class _Server:
        def run(self, **kwargs):
            calls.update(kwargs)

    monkeypatch.setenv("AURA_PORT", "8100")
    monkeypatch.setattr(entrypoint, "build_server", lambda gateway: _Server())
    entrypoint.main()
    assert calls == {"transport": "http", "host": "127.0.0.1", "port": 8100, "show_banner": False}
