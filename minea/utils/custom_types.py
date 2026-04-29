from typing import NamedTuple


class TcpConfig(NamedTuple):
    """Data required to use TCP/IP socket."""

    host: str
    port: int


class CommandConfig(NamedTuple):
    """Constants for sending/receiving commands."""

    sep: str
    """Character to separate command and arg values."""
