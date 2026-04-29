from pathlib import Path
from typing import Optional
from .utils import ConfigManager, TcpConfig, CommandConfig


class Services:
    """Class to manage objects that MINEA requires."""

    def __init__(self, config_file: Optional[Path] = None):

        self._config_manager = ConfigManager(config_file)
        self._tcp_config: TcpConfig = self.config_manager.get_tcp_config()
        self._cmd_config: CommandConfig = self.config_manager.get_command_config()

    @property
    def config_manager(self) -> ConfigManager:
        """Return ConfigManager object."""
        return self._config_manager

    @property
    def tcp_config(self) -> TcpConfig:
        """Return TcpConfig object."""
        return self._tcp_config

    @property
    def cmd_config(self) -> CommandConfig:
        """Return CommandConfig object."""
        return self._cmd_config
