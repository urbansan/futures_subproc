import pytest
from shell_multiprocess.async_processor import AsyncProcessor


@pytest.mark.asyncio
async def test_runs_echos():
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
    processor = AsyncProcessor(4, cmds)

    await processor.start()
    assert 8 == len(processor.process_pool)
    assert 0 == processor.returncode


@pytest.mark.asyncio
async def test_run_false():
    cmds = [
        "false",
    ]
    processor = AsyncProcessor(4, cmds)

    await processor.start()
    assert 1 == len(processor.process_pool)
    assert 0 != processor.returncode


@pytest.mark.asyncio
async def test_run_shell_syntax():
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
    processor = AsyncProcessor(4, cmds)

    await processor.start()
    assert 8 == len(processor.process_pool)
    assert 1 == processor.returncode
