from shell_multiprocess.cmdline_args import parser
import pytest


def test_file_exists(files_path):
    args = parser.get_parsed_cmdline_args(["files/tasks.list", "4"])
    expected_path = files_path / "tasks.list"
    assert expected_path.absolute() == args.filename.absolute()
    assert 4 == args.processes
    assert False is args.soft_kill


def test_file_does_not_exist():
    with pytest.raises(SystemExit):
        parser.get_parsed_cmdline_args(["does_not_exist", "4"])


def test_workers_not_int():
    with pytest.raises(SystemExit):
        parser.get_parsed_cmdline_args(["tests/files/tasks.list", "zzz"])


def test_soft_kill(files_path):
    args = parser.get_parsed_cmdline_args(["files/tasks.list", "4", "-s"])
    expected_path = files_path / "tasks.list"
    assert expected_path.absolute() == args.filename.absolute()
    assert 4 == args.processes
    assert True is args.soft_kill
