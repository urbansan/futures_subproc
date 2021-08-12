import sys
import asyncio
from .async_processor import AsyncProcessor
from .cleanup import CleanupAsyncProcessor
from . import interpreter


def main():
    args = interpreter.get_args()

    loop = asyncio.get_event_loop()
    processor = AsyncProcessor(args.process_count, args.shell_commands)
    try:
        loop.run_until_complete(processor.start())
        print(processor.filelogger.get_log_str())
    except KeyboardInterrupt:
        processor.stop()
        print("multiprocess: cleaning up started processes...", file=sys.stderr)
        cleanup = CleanupAsyncProcessor(processor, loop, args.kill_signal)
        loop.run_until_complete(cleanup.start())
    finally:
        loop.close()
        exit(processor.returncode)
