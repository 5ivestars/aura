"""Errori del dominio, indipendenti dal protocollo MCP."""


class GatewayError(Exception):
    """Errore nella comunicazione con l'impianto."""


class AccessDeniedError(GatewayError):
    """L'utente non è autenticato o non ha i permessi necessari."""


class NotFoundError(GatewayError):
    """L'impianto o il dispositivo richiesto non esiste o non è accessibile."""


class ConfigError(ValueError):
    """La configurazione letta dalle variabili d'ambiente non è valida."""
