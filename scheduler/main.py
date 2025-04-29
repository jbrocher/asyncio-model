import time

from scheduler.future import Sleep
from scheduler.scheduler import Scheduler


def sleep():
    print("waiting for result before ping...")
    return (yield Sleep(5))


def ping():
    result = yield sleep()
    print(f"result: {result}")
    while True:
        print("ping")
        time.sleep(1)
        yield


def pong():
    while True:
        print("pong")
        time.sleep(1)
        yield


if __name__ == "__main__":
    scheduler = Scheduler()
    scheduler.create_task(ping())
    scheduler.create_task(pong())
    scheduler.run_forever()
