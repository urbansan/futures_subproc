import subprocess
import threading
import time
import psutil
import signal
from typing import List


def test_soft_kill():
    cmd = ("multiprocess files/immuner.list 2 --soft-kill",)
    alive_processes_cmds, returncode = run_processes(cmd)
    assert returncode != 0
    assert alive_processes_cmds
    assert all(["immuner.py" in c for c in alive_processes_cmds]), alive_processes_cmds


def test_hard_kill():
    cmd = ("multiprocess files/immuner.list 2",)
    alive_processes_cmds, returncode = run_processes(cmd)
    assert returncode != 0
    assert not alive_processes_cmds


def _get_child_processes(parent_pid, recursive=False) -> List[psutil.Process]:
    try:
        parent = psutil.Process(parent_pid)
    except psutil.NoSuchProcess:
        return []
    try:
        child_processes = parent.children(recursive=recursive)
    except psutil.NoSuchProcess:
        pass
    else:
        return [process for process in child_processes]


def _get_live_processes(pids):
    existing_processes = []
    for pid in pids:
        try:
            p = psutil.Process(pid)
        except psutil.NoSuchProcess:
            pass
        else:
            # print(p.cmdline())
            existing_processes.append(p)
    return existing_processes


def interrupt(popen: subprocess.Popen, alive_processes_cmds: list):
    # waiting until multiprocess is set up and run subprocesses
    waited = 0.0
    step = 0.1
    while waited <= 1.0:
        time.sleep(step)
        waited += step
        if all(proc.status() == "sleeping" for proc in _get_child_processes(popen.pid)):
            break

    all_pids = [p.pid for p in _get_child_processes(popen.pid, True)]
    for proc in _get_child_processes(popen.pid):
        proc.send_signal(signal.SIGINT)

    # waiting until multiprocess dies
    waited = 0.0
    step = 0.1
    while waited <= 1.0:
        time.sleep(step)
        waited += step
        if not _get_child_processes(popen.pid):
            break

    cmds = [" ".join(p.cmdline()) for p in _get_live_processes(all_pids)]
    alive_processes_cmds += cmds


def run_processes(cmd):
    popen = subprocess.Popen(cmd, shell=True)
    alive_processes_cmds = []
    th = threading.Thread(target=interrupt, args=(popen, alive_processes_cmds))
    th.start()
    popen.communicate()

    th.join()
    return alive_processes_cmds, popen.returncode
