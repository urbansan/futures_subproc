from shell_multiprocess.launcher import Launcher
import pytest


def test_file_exists(files_path):
    args = Launcher().parser.parse_args(["files/tasks.list", "4"])
    expected_path = files_path / "tasks.list"
    assert expected_path.absolute() == args.filename.absolute()
    assert 4 == args.processes


def test_file_does_not_exist():
    with pytest.raises(SystemExit):
        Launcher().parser.parse_args(["does_not_exist", "4"])


def test_workers_not_int():
    with pytest.raises(SystemExit):
        args = Launcher().parser.parse_args(["tests/files/tasks.list", "zzz"])
