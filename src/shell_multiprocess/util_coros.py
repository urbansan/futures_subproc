import asyncio
from typing import Iterable


async def confirm_process_statuses(pids: Iterable):
    process_objs = []
    for pid in pids:
        cmd = f"ps -l -p {pid} | grep {pid} > /dev/null"
        process_obj = await asyncio.create_subprocess_shell(cmd)
        process_obj.checked_pid = pid
        process_objs.append(process_obj)
    finished, pending = await asyncio.wait([p.wait() for p in process_objs])
    for p in process_objs:
        print(p.checked_pid, "is dead" if bool(p.returncode) else "is alive")
