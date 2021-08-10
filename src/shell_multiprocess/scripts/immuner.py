from time import sleep
import sys, os


def start():
    time_to_sleep = int(sys.argv[1])
    for _ in range(time_to_sleep + 1):
        try:
            sleep(1)
            print(os.getpid(), "immuner")
        except KeyboardInterrupt:
            print(f"immuner {time_to_sleep} tried to be killed")

    print("slept", time_to_sleep)
