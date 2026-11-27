import pytest

from aura.config import Settings
from aura.errors import ConfigError


def test_defaults_without_variables():
    assert Settings.from_env({}) == Settings(
        backend="fake", host="127.0.0.1", port=8000, log_level="INFO"
    )


def test_reads_and_normalizes_variables():
    env = {
        "AURA_BACKEND": " KNX ",
        "AURA_HOST": "0.0.0.0",
        "AURA_PORT": "9000",
        "AURA_LOG_LEVEL": "debug",
    }
    assert Settings.from_env(env) == Settings(
        backend="knx", host="0.0.0.0", port=9000, log_level="DEBUG"
    )


def test_empty_host_falls_back_to_default():
    assert Settings.from_env({"AURA_HOST": "  "}).host == "127.0.0.1"


def test_reads_process_environment(monkeypatch):
    monkeypatch.setenv("AURA_PORT", "8123")
    assert Settings.from_env().port == 8123


@pytest.mark.parametrize(
    ("env", "message"),
    [
        ({"AURA_BACKEND": "cloud"}, "AURA_BACKEND"),
        ({"AURA_LOG_LEVEL": "verbose"}, "AURA_LOG_LEVEL"),
        ({"AURA_PORT": "abc"}, "numero"),
        ({"AURA_PORT": "0"}, "tra 1 e 65535"),
        ({"AURA_PORT": "70000"}, "tra 1 e 65535"),
    ],
)
def test_rejects_invalid_values(env, message):
    with pytest.raises(ConfigError, match=message):
        Settings.from_env(env)
