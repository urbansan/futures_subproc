from shell_multiprocess.async_processor import AsyncProcessor
import asyncio


async def keyboard_interrupt_task():
    await asyncio.sleep(0.1)
    raise KeyboardInterrupt("Test interruption")


LOOP = asyncio.get_event_loop()


def test_abort():
    cmds = [
        "sleep 99",
        "sleep 1",
        "sleep 1",
    ]
    processor = AsyncProcessor(4)
    task = asyncio.ensure_future(keyboard_interrupt_task())
    processor.pending.add(task)
    try:
        LOOP.run_until_complete(processor.start(cmds))
    except KeyboardInterrupt:
        processor.stop()
    assert 3 == len(processor.process_pool)
    assert 0 != processor.returncode
