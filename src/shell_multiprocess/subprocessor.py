import os
import subprocess
import signal
import psutil
from functools import reduce

from concurrent.futures import Future, ThreadPoolExecutor, as_completed


class SubProcessor:
    def __init__(self, commands, worker_count):
        self._processes = []
        self._futures = []
        self.commands = commands
        self.worker_count = worker_count

    def _task(self, cmd):
        p = subprocess.Popen(cmd.strip(), env=os.environ, shell=True)
        self._processes.append(p)
        return p.communicate()

    @staticmethod
    def _kill_child_processes(parent_pid, sig=signal.SIGTERM):
        try:
            parent = psutil.Process(parent_pid)
        except psutil.NoSuchProcess:
            return
        children = parent.children(recursive=True)
        for process in children:
            process.send_signal(sig)

    def run(self):
        with ThreadPoolExecutor(
            self.worker_count, thread_name_prefix=type(self).__name__
        ) as pool:
            # with file.open("r") as f:
            self._futures = [pool.submit(self._task, cmd=cmd) for cmd in self.commands]
            for future in as_completed(self._futures):
                future.result()

        return 1 if any(p.returncode for p in self._processes) else 0

    def abort(self):
        for future in self._futures:
            print(future.cancel())
        for process in self._processes:
            self._kill_child_processes(process.pid)
            process.kill()
