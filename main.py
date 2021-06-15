import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed, Future
from pathlib import Path
import os

import threading

workers = int(sys.argv[1])
file = Path(sys.argv[2])

processes = []

def task(cmd):
    p = subprocess.Popen(cmd.strip(), env=os.environ, shell=True)
    processes.append(p)
    return p.communicate()
#
# broken = False
# import threading
# import time
# def monitor():
#     while True:
#         if broken == True:
#             break
#         time.sleep(0.25)
#
#         print(*(f'{p.pid!s}: {p.poll()}' for p in processes), sep=', ')
#
# monitor_thread = threading.Thread(target=monitor)
#
# monitor_thread.start()

import signal, psutil
def kill_child_processes(parent_pid, sig=signal.SIGTERM):
    try:
      parent = psutil.Process(parent_pid)
    except psutil.NoSuchProcess:
      return
    children = parent.children(recursive=True)
    for process in children:
      process.send_signal(sig)

with ThreadPoolExecutor(workers, thread_name_prefix='hadouken') as pool:
    with file.open('r') as f:
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
