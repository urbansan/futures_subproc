from typing import List
from .async_file_logger import AsyncFileLogger


class AsyncDispatcher:
    def __init__(self, cmds: List[str], disable_logging=False):
        self.cmds = cmds
        self.filelogger = AsyncFileLogger(cmds, disable_logging=disable_logging)

    def callback(self, future: asyncio.Future, index: int):
        logline = self.loglines[index]
        logline.set_end()
        self.print_all_lines()

    def print_all_lines(self):
        for line in self.loglines:
            print(line.formatted())

    async def get_subprocess_future(self, cmd, index):
        process_obj = await asyncio.subprocess.create_subprocess_shell(cmd)
        future = asyncio.ensure_future(process_obj.wait())
        self.loglines[index].set_start()
        future.add_done_callback(partial(self.callback, index=index))
        return future

    async def get_tasks(self):
        return [
            await self.get_subprocess_future(cmd, idx)
            for idx, cmd in enumerate(self.cmds)
        ]
