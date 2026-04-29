#!/usr/bin/env python3

import socket
from typing import Sequence
from string import Template
import argparse

from minea.utils import TcpConfig, CommandConfig, ConfigManager

_config_manager: ConfigManager = ConfigManager()
TCP_CONFIG = _config_manager.get_tcp_config()
CMD_CONFIG = _config_manager.get_command_config()

_cmds = ["echo"]


class InvalidCmdError(Exception):

    msg_template = Template(f"Invalid MINEA command '$cmd'. Valid values are: {', '.join(_cmds)}")


def _make_cmd_str(cmd: str, args: Sequence[str]) -> bytes:

    args_str = CMD_CONFIG.sep.join(args)
    if args_str:
        args_str = f"{CMD_CONFIG.sep}{args_str}"

    s = f"{cmd}{args_str}"

    return s.encode()


def _validate_cmd(cmd):
    if cmd not in _cmds:
        raise InvalidCmdError(InvalidCmdError.msg_template.substitute(cmd))


def send_cmd_tcp(cmd: str, *args):
    """Send command `cmd` over TCP connection to GUI."""

    _validate_cmd(cmd)

    cmd_bytes = _make_cmd_str(cmd, args)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(TCP_CONFIG)
        s.sendall(cmd_bytes)


def _parse_cl_args(cl_args) -> argparse.Namespace:
    parser = argparse.ArgumentParser("Send command to MINEA")
    parser.add_argument("cmd", help="Command to run")
    parser.add_argument("cmd_args", help="Any args for `cmd`", nargs="*")

    return parser.parse_args(cl_args)


if __name__ == "__main__":

    import sys

    args = _parse_cl_args(sys.argv[1:])

    send_cmd_tcp(args.cmd, *args.cmd_args)
