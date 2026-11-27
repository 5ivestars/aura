import pytest
from fastmcp import Client
from fastmcp.exceptions import ToolError

from aura.config import Settings
from aura.fake_gateway import FakeGateway
from aura.knx_gateway import KnxIotGateway
from aura.server import build_server

pytestmark = pytest.mark.anyio

EXPECTED_TOOLS = {"check_access", "list_installations", "list_lights", "get_light_state"}


async def test_exposes_read_only_tools(server):
    async with Client(server) as client:
        tools = await client.list_tools()
    assert {tool.name for tool in tools} == EXPECTED_TOOLS
    for tool in tools:
        assert tool.description
        assert tool.annotations.read_only_hint is True
        assert tool.annotations.destructive_hint is False


async def test_instructions_reach_the_client(server):
    async with Client(server) as client:
        assert "list_installations" in client.instructions


async def test_check_access(server):
    async with Client(server) as client:
        result = await client.call_tool("check_access")
    assert result.structured_content["connected"] is True


async def test_full_flow_to_light_state(server):
    async with Client(server) as client:
        installations = (await client.call_tool("list_installations")).structured_content
        installation_id = installations["result"][0]["id"]
        lights = (
            await client.call_tool("list_lights", {"installation_id": installation_id})
        ).structured_content["result"]
        kitchen = next(light for light in lights if light["room"] == "Cucina")
        state = (
            await client.call_tool(
                "get_light_state", {"installation_id": installation_id, "light_id": kitchen["id"]}
            )
        ).structured_content
    assert state == {"id": "luce-2", "name": "Luce cucina", "room": "Cucina", "is_on": False}


async def test_domain_errors_become_tool_errors(server):
    async with Client(server) as client:
        with pytest.raises(ToolError, match="non esiste"):
            await client.call_tool(
                "get_light_state", {"installation_id": "kit-demo", "light_id": "luce-9"}
            )


async def test_access_denied_is_reported():
    server = build_server(FakeGateway.with_demo_data(connected=False))
    async with Client(server) as client:
        with pytest.raises(ToolError, match="Accesso"):
            await client.call_tool("list_installations")


async def test_missing_implementation_is_reported():
    server = build_server(KnxIotGateway(Settings(backend="knx")))
    async with Client(server) as client:
        with pytest.raises(ToolError, match="non ancora disponibile"):
            await client.call_tool("check_access")


class _BrokenGateway(FakeGateway):
    async def list_installations(self):
        raise RuntimeError("dettaglio interno da non mostrare")


async def test_unexpected_errors_are_masked():
    server = build_server(_BrokenGateway([]))
    async with Client(server) as client:
        with pytest.raises(ToolError) as error:
            await client.call_tool("list_installations")
    assert "dettaglio interno" not in str(error.value)
