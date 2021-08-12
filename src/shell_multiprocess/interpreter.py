from . import parser
from pathlib import Path
import signal
from typing import List
from dataclasses import dataclass
import signal


@dataclass
class Args:
    shell_commands: List[str]
    process_count: int
    kill_signal: signal.Signals


def get_args() -> Args:
    args = parser.get_args()
    cmds = _read_cmds(args.filename)
    kill_signal = _choose_signal(args.soft_kill)
    return Args(cmds, args.processes, kill_signal)


def _read_cmds(filepath: Path):
    with filepath.open("r") as f:
        cmds = [line.strip() for line in f.readlines()]
    return cmds


def _choose_signal(is_sigint):
    return signal.SIGINT if is_sigint else signal.SIGKILL
