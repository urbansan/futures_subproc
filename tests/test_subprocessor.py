from shell_multiprocess.subprocessor import SubProcessor


def test_runs_echos():
    cmds = [
        "echo 1",
        "echo 2",
        "echo 3",
        "echo 4",
        "echo 5",
        "echo 6",
        "echo 7",
        "echo 8",
    ]
    processor = SubProcessor(cmds, 4)

    returncode = processor.run()
    assert 8 == len(processor._processes)
    assert 0 == returncode


def test_run_false():
    cmds = [
        "false",
    ]
    processor = SubProcessor(cmds, 4)

    returncode = processor.run()
    assert 1 == len(processor._processes)
    assert 0 != returncode


def test_run_shell_syntax():
    cmds = [
        "echo 1 && true",
        "echo 2 && false",
        "echo 3 && true",
        "echo 4 && true",
        "echo 5; false",
        "echo 6 && true",
        "echo 7 && false",
        "echo 8 || true",
    ]
    processor = SubProcessor(cmds, 4)

    returncode = processor.run()
    assert 8 == len(processor._processes)
    assert 1 == returncode


def test_cancel():
    cmds = [
        "sleep 1",
    ]
    processor = SubProcessor(cmds, 4)

    returncode = processor.run()
    assert 1 == len(processor._processes)
    assert 0 != returncode