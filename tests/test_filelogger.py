import pytest
from shell_multiprocess.async_file_logger import AsyncFileLogger


@pytest.mark.asyncio
async def test_logger_creates_file_and_updates_it(tmpdir):
    logpath = tmpdir / "test.log"
    cmds = ["true", "false"]
    logger = AsyncFileLogger(cmds, logpath)
    assert not logpath.exists()
    await logger.start(0)
    assert logpath.exists()

    with logpath.open("r") as f:
        log_content: str = f.read()

    assert "true" in log_content
    assert "false" in log_content
    assert log_content.count("\n") == 4
