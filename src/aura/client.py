"""Client MCP minimo da riga di comando, per provare il server senza un servizio AI.

Esempi:
    aura-client tools
    aura-client call list_installations
    aura-client call get_light_state --arg installation_id=kit-demo --arg light_id=luce-1
"""

import argparse
import asyncio
import json
import sys
from typing import Any

from fastmcp import Client

DEFAULT_URL = "http://127.0.0.1:8000/mcp"


def _parse_args(argv: list[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog="aura-client", description="Client MCP di AURA.")
    parser.add_argument("--url", default=DEFAULT_URL, help=f"URL del server MCP ({DEFAULT_URL}).")
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("tools", help="Elenca gli strumenti esposti dal server.")
    call = commands.add_parser("call", help="Chiama uno strumento.")
    call.add_argument("tool", help="Nome dello strumento.")
    call.add_argument(
        "--arg",
        action="append",
        default=[],
        metavar="NOME=VALORE",
        help="Argomento dello strumento; si può ripetere.",
    )
    return parser.parse_args(argv)


def _parse_tool_args(pairs: list[str]) -> dict[str, str]:
    arguments: dict[str, str] = {}
    for pair in pairs:
        name, sep, value = pair.partition("=")
        if not sep or not name:
            raise SystemExit(f"Argomento non valido: '{pair}'. Usare NOME=VALORE.")
        arguments[name] = value
    return arguments


async def run(argv: list[str] | None = None, transport: Any = None) -> int:
    """Esegue il comando; `transport` permette ai test di passare il server in memoria."""
    args = _parse_args(argv)
    async with Client(transport or args.url) as client:
        if args.command == "tools":
            for tool in await client.list_tools():
                print(f"{tool.name}: {tool.description}")
            return 0
        result = await client.call_tool(args.tool, _parse_tool_args(args.arg), raise_on_error=False)
        if result.is_error:
            message = " ".join(getattr(item, "text", "") for item in result.content)
            print(f"Errore: {message}", file=sys.stderr)
            return 1
        print(json.dumps(result.structured_content, ensure_ascii=False, indent=2))
        return 0


def main() -> None:
    """Punto di ingresso di `aura-client`."""
    raise SystemExit(asyncio.run(run()))
