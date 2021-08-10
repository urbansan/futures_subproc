import sys
import asyncio
from .async_processor import AsyncProcessor
from .cleanup import CleanupAsyncProcessor
from .launcher import Launcher


def main():
    cmds, process_count = Launcher().get_cmds_and_proc_count()

    loop = asyncio.get_event_loop()
    processor = AsyncProcessor(process_count)
    try:
        loop.run_until_complete(processor.start(cmds))
    except KeyboardInterrupt:
        processor.stop()
        print("multiprocess: cleaning up started processes...", file=sys.stderr)
        cleanup = CleanupAsyncProcessor(processor, loop)
        loop.run_until_complete(cleanup.start())
    finally:
        loop.close()
        exit(processor.returncode)
