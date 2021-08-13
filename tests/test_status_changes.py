import subprocess
import threading
import time
import psutil
import signal
from typing import List


def test_logging_when_interrupted():
    cmd = "multiprocess files/immuner.list 1"
    out, err = run_processes(cmd, interrupt_delay=0.5)
    out_str = out.decode()
    assert out_str.count("interrupted") == 1
    assert out_str.count("never-ran") == 1


def test_logging_task_with_error():
    cmd = "multiprocess files/true_false.list 1"
    out, err = run_processes(cmd)
    out_str = out.decode()
    assert out_str.count("done") == 1
    assert out_str.count("error") == 1


def test_logging_successes():
    cmd = "multiprocess files/tasks.list 1"
    out, err = run_processes(cmd)
    out_str: str = out.decode()
    assert out_str.count("done") == 8


def run_processes(cmd, interrupt_delay: float = None):
    popen = subprocess.Popen(
        cmd.split(), shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    th = threading.Thread(target=_interrupt, args=(popen, interrupt_delay))
    if _interrupt is not None:
        th.start()
    out, err = popen.communicate()
    if _interrupt is not None:
        th.join()
    return out, err


def _interrupt(popen: subprocess.Popen, delay: float):
    waited = 0.0
    step = 0.1
    proc = psutil.Process(popen.pid)
    while waited <= delay:
        time.sleep(step)
        waited += step
        if proc.status() == "sleeping":
            break
    print("waited", str(waited), "seconds to interrupt")
    popen.send_signal(signal.SIGINT)



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
