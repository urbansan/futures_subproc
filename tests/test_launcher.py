from shell_multiprocess.launcher import Launcher
import argparse
import pytest
from pathlib import Path


def test_file_exists():
    args = Launcher().parser.parse_args(["tests/test_launcher.py", "4"])
    assert Path(__file__).absolute() == args.filename.absolute()
    assert 4 == args.processes


def test_file_does_not_exist():
    with pytest.raises(SystemExit):
        Launcher().parser.parse_args(["tests/does_not_exist", "4"])

def test_workers_not_int():
    with pytest.raises(SystemExit):
        args = Launcher().parser.parse_args(["tests/test_launcher.py", "zzz"])
