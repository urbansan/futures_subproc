import asyncio
from collections import deque
from typing import List, Set


class AsyncProcessor:
    def __init__(self, process_count):
        self._process_count = process_count
        self.process_pool: List[asyncio.subprocess.Process] = []
        self.pending: Set[asyncio.Task] = set()
        self.stopped = False

    @property
    def process_count(self):
        return self._process_count

    def stop(self):
        self.stopped = True

    @property
    def returncode(self):
        if any(p.returncode for p in self.process_pool if p.returncode is not None):
            return 1
        if any(p.returncode is None for p in self.process_pool):
            return 2
        return 0

    async def start(self, cmds: list):
        pending = await self._get_pending_tasks(cmds[: self.process_count])
        self.pending.update(pending)
        remaining_cmds = deque(cmds[self.process_count :])

        while remaining_cmds and not self.stopped:
            finished, self.pending = await asyncio.wait(
                self.pending, return_when=asyncio.FIRST_COMPLETED
            )
            if self.stopped:
                return

            new_cmds = self._pop_cmds(remaining_cmds, len(finished))
            new_tasks = await self._get_pending_tasks(new_cmds)
            self.pending.update(new_tasks)

        for f in asyncio.as_completed(self.pending):
            await f
            if self.stopped:
                return

    @staticmethod
    def _pop_cmds(cmds: deque, no_elements_to_pop: int):
        poped_cmds = []
        for _ in range(no_elements_to_pop):
            try:
                cmd = cmds.popleft()
            except IndexError:
                break
            else:
                poped_cmds.append(cmd)
        return poped_cmds

    async def _get_pending_tasks(self, cmds):
        process_obj_futures = {self._get_subprocess_future(cmd) for cmd in cmds}
        finished, _ = await asyncio.wait(process_obj_futures)
        pending = {f.result() for f in finished}
        return pending

    async def _get_subprocess_future(self, cmd):
        process_obj = await asyncio.subprocess.create_subprocess_shell(cmd)
        self.process_pool.append(process_obj)
        task = asyncio.ensure_future(process_obj.wait())
        return task


#
#
# cmds = [
#     "sleep 1; date && echo 4a",
#     "sleep 1; date && echo 4b",
#     "sleep 1; date && echo 31c",
#     "sleep 1; date && echo 3false && false",
#     "sleep 100; date && echo 3b",
#     "sleep 100; date && echo 3c",
#     "sleep 100; date && echo 3d",
# ]
