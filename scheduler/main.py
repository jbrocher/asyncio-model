import time

from scheduler.scheduler import Scheduler


def ping():
    while True:
        print("ping")
        time.sleep(1)
        (yield)


def pong():
    while True:
        print("pong")
        time.sleep(1)
        (yield)


if __name__ == "__main__":
    scheduler = Scheduler()
    scheduler.create_task(ping())
    scheduler.create_task(pong())
    scheduler.run_forever()
