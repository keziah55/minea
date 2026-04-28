import tomllib
from pathlib import Path
from typing import Optional


class ConfigManager:
    """
    Class to manage reading from `config.toml` file.

    Parameters
    ----------
    config_file
        Optionally provide path to config toml file. If not given, defaults to `config.toml`
        in project root.
    """

    def __init__(self, config_file: Optional[Path] = None):

        if config_file is None:
            config_file = Path(__file__).parents[2].joinpath("config.toml")

        if not config_file.exists():
            raise FileNotFoundError(f"No such file config file {config_file}")
        self._config_file = config_file

        self._config_data = self._get_config()

    def _get_config(self) -> dict:
        """Read config file."""

        with open(self._config_file, "rb") as fileobj:
            config_data = tomllib.load(fileobj)

        return config_data

    def get_config_section(self, key: str) -> dict:
        """Get section from config."""

        data = self._config_data.get(key, None)

        if data is None:
            raise KeyError(f"Unknown config key '{key}'")

        return data
