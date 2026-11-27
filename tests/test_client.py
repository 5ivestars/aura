import json

import pytest

from aura import client

pytestmark = pytest.mark.anyio


async def test_lists_tools(server, capsys):
    assert await client.run(["tools"], transport=server) == 0
    output = capsys.readouterr().out
    assert "list_installations:" in output
    assert "get_light_state:" in output


async def test_calls_tool_with_arguments(server, capsys):
    argv = [
        "call",
        "get_light_state",
        "--arg",
        "installation_id=kit-demo",
        "--arg",
        "light_id=luce-1",
    ]
    assert await client.run(argv, transport=server) == 0
    assert json.loads(capsys.readouterr().out)["is_on"] is True


async def test_reports_tool_errors(server, capsys):
    argv = ["call", "list_lights", "--arg", "installation_id=altro"]
    assert await client.run(argv, transport=server) == 1
    assert "non esiste" in capsys.readouterr().err


async def test_rejects_malformed_arguments(server):
    with pytest.raises(SystemExit, match="NOME=VALORE"):
        await client.run(["call", "list_lights", "--arg", "senza-uguale"], transport=server)


def test_main_runs_the_command(monkeypatch):
    async def fake_run():
        return 0

    monkeypatch.setattr(client, "run", fake_run)
    with pytest.raises(SystemExit) as exit_info:
        client.main()
    assert exit_info.value.code == 0
