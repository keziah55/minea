from pathlib import Path
from typing import Optional
from .utils import ConfigManager


class Services:
    """Class to manage objects that MINEA requires."""

    def __init__(self, config_file: Optional[Path] = None):

        self.config_manager = ConfigManager(config_file)
