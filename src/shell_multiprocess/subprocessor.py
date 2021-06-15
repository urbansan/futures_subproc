import os
import subprocess
import sys
import signal
import psutil

import threading
from concurrent.futures import Future, ThreadPoolExecutor, as_completed
from pathlib import Path

workers = int(sys.argv[1])
file = Path(sys.argv[2])


class Subprocessor:
    def __init__(self, commands, worker_count):
        self._processes = []
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
            workers, thread_name_prefix=type(self).__name__
        ) as pool:
            # with file.open("r") as f:
            futures = [pool.submit(self._task, cmd=cmd) for cmd in self.commands]
            try:
                for future in as_completed(futures):
                    future.result()
            except KeyboardInterrupt:
                for future in futures:
                    print(future.cancel())
                for process in self._processes:
                    self._kill_child_processes(process.pid)
                    process.kill()
