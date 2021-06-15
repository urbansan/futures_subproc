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

processes = []


def task(cmd):
    p = subprocess.Popen(cmd.strip(), env=os.environ, shell=True)
    processes.append(p)
    return p.communicate()


def kill_child_processes(parent_pid, sig=signal.SIGTERM):
    try:
        parent = psutil.Process(parent_pid)
    except psutil.NoSuchProcess:
        return
    children = parent.children(recursive=True)
    for process in children:
        process.send_signal(sig)


with ThreadPoolExecutor(workers, thread_name_prefix="hadouken") as pool:
    with file.open("r") as f:
        futures = [pool.submit(task, cmd=cmd) for cmd in f.readlines()]
    try:
        for future in as_completed(futures):
            future.result()
    except KeyboardInterrupt:
        for future in futures:
            print(future.cancel())
        for process in processes:
            kill_child_processes(process.pid)
            process.kill()
# time.sleep(0.3)
# broken = True
# monitor_thread.join()
