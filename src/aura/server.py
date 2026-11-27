"""Server MCP di AURA: espone le operazioni sull'impianto come strumenti MCP."""

from collections.abc import Awaitable
from typing import Annotated

from fastmcp import FastMCP
from fastmcp.exceptions import ToolError
from pydantic import Field

from aura import __version__
from aura.domain import AccessStatus, Installation, Light, LightState
from aura.errors import GatewayError
from aura.gateway import InstallationGateway

INSTRUCTIONS = (
    "AURA permette di consultare gli impianti domotici Vimar dell'utente. "
    "Per rispondere su un dispositivo, trova prima l'impianto con list_installations "
    "e la luce con list_lights, poi usa gli id restituiti: non inventarli. "
    "Se una richiesta fallisce per un problema di accesso, verifica con check_access."
)

# Gli strumenti di questo PoC leggono soltanto: non modificano l'impianto.
READ_ONLY = {"readOnlyHint": True, "destructiveHint": False, "idempotentHint": True}

InstallationId = Annotated[
    str, Field(description="Id dell'impianto, come restituito da list_installations.")
]
LightId = Annotated[str, Field(description="Id della luce, come restituito da list_lights.")]


async def _call[T](operation: Awaitable[T]) -> T:
    """Esegue un'operazione sull'impianto e traduce gli errori del dominio in errori MCP."""
    try:
        return await operation
    except GatewayError as error:
        raise ToolError(str(error)) from error
    except NotImplementedError as error:
        raise ToolError("Funzione non ancora disponibile con la configurazione attuale.") from error


def build_server(gateway: InstallationGateway) -> FastMCP:
    """Crea il server MCP che usa l'implementazione dell'impianto ricevuta."""
    mcp = FastMCP(
        name="AURA",
        instructions=INSTRUCTIONS,
        version=__version__,
        mask_error_details=True,
    )

    @mcp.tool(annotations=READ_ONLY)
    async def check_access() -> AccessStatus:
        """Verifica se AURA riesce ad accedere agli impianti dell'utente."""
        return await _call(gateway.check_access())

    @mcp.tool(annotations=READ_ONLY)
    async def list_installations() -> list[Installation]:
        """Elenca gli impianti domotici a cui l'utente ha accesso."""
        return await _call(gateway.list_installations())

    @mcp.tool(annotations=READ_ONLY)
    async def list_lights(installation_id: InstallationId) -> list[Light]:
        """Elenca le luci di un impianto, con il nome e l'ambiente in cui si trovano."""
        return await _call(gateway.list_lights(installation_id))

    @mcp.tool(annotations=READ_ONLY)
    async def get_light_state(installation_id: InstallationId, light_id: LightId) -> LightState:
        """Indica se una luce dell'impianto è accesa o spenta."""
        return await _call(gateway.get_light_state(installation_id, light_id))

    return mcp
