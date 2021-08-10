import asyncio
from .async_processor import AsyncProcessor
from .launcher import Launcher


def main():
    cmds, process_count = Launcher().get_cmds_and_proc_count()

    loop = asyncio.get_event_loop()
    processor = AsyncProcessor(process_count)
    try:
        loop.run_until_complete(processor.start(cmds))
    except KeyboardInterrupt:
        processor.stop()
        print(*[f"{p.pid}:{p.returncode}" for p in processor.process_pool])
    finally:
        loop.close()
        exit(processor.returncode)
