import pytest

from aura.fake_gateway import FakeGateway
from aura.server import build_server


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.fixture
def gateway():
    return FakeGateway.with_demo_data()


@pytest.fixture
def server(gateway):
    return build_server(gateway)
