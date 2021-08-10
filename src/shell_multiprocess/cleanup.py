import sys
import asyncio
import psutil
import concurrent.futures
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .async_processor import AsyncProcessor


class CleanupAsyncProcessor:
    """Cleanup class for AsyncProcessor if there would be any processes
    which would be troublesome to kill. Currently the KeyInterruptError
    cancels and kills all shell processes but that might be too optimistic
    when a process is KeyInterruptError-proof and requires a forced cleanup.

    The event loop cannot be stopped before running cleanup.

    Example usage:

    loop = asyncio.get_event_loop()
    processor = AsyncProcessor(2)
    try:
        loop.run_until_complete(processor.start(cmds))
    except KeyboardInterrupt:
        processor.stop()
        cleanup = CleanupAsyncProcessor(processor, loop)
        loop.run_until_complete(cleanup.start())
    finally:
        loop.close()
        exit(processor.returncode)
    """

    def __init__(self, processor: "AsyncProcessor", loop: asyncio.AbstractEventLoop):
        self.processor = processor
        if not self.processor.stopped:
            print("Processor was not stopped. Force stopping", file=sys.stderr)
            self.processor.stop()
        self.loop = loop

    async def start(self):
        # print("starting cleanup", file=sys.stderr)
        self._cancel_pending()
        await self._cleanup_children()
        await self._cleanup_parents()

    def _get_executor(self):
        return concurrent.futures.ThreadPoolExecutor(
            max_workers=self.processor.process_count
        )

    def _cancel_pending(self):
        for future in self.processor.pending:
            future.cancel()
            # print(
            #     *[f"{p.pid}-{p.returncode}" for p in self.processor.process_pool],
            #     file=sys.stderr,
            # )

    async def _cleanup_children(self):
        child_proc_tasks = set()
        executor = self._get_executor()
        for process_obj in self.processor.process_pool:
            task = self.loop.run_in_executor(
                executor, self._kill_child_processes, process_obj.pid
            )
            child_proc_tasks.add(task)
        await asyncio.wait(child_proc_tasks)

    async def _cleanup_parents(self):
        for process_obj in self.processor.process_pool:
            try:
                process_obj.kill()
            except ProcessLookupError:
                pass
                # print(process_obj, "already killed", file=sys.stderr)
            # else:
                # print(f"killing pid {process_obj.pid}", file=sys.stderr)
        finished, pending = await asyncio.wait(
            [p.wait() for p in self.processor.process_pool]
        )

    @staticmethod
    def _kill_child_processes(parent_pid):
        # print(f"trying killing kid for parent {parent_pid}", file=sys.stderr)
        try:
            parent = psutil.Process(parent_pid)
        except psutil.NoSuchProcess:
            return
        try:
            child_processes = parent.children(recursive=True)
        except psutil.NoSuchProcess:
            pass
        else:
            for process in child_processes:
                # print("killing child pid", process.pid, file=sys.stderr)
                process.kill()
