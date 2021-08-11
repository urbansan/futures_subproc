import time
import sys, os


def immuner():
    start = time.time()
    remaining = total = float(sys.argv[1])
    while True:
        try:
            time.sleep(remaining)
            break
        except KeyboardInterrupt:
            remaining = total - (time.time() - start)
            elapsed = total - remaining
            if remaining <= 0.0:
                break
            print(
                f"immuner with pid {os.getpid()} tried to be killed after "
                f"{round(elapsed, 2)}s. Remaining {round(remaining, 2)}s"
            )

    print(f"pid {os.getpid()} slept in {total}s")


if __name__ == "__main__":
    immuner()
