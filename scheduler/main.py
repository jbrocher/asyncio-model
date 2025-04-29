from scheduler.future import Sleep
import time
from scheduler.scheduler import Scheduler


async def sleep(n: int):
    return await Sleep(n)


async def ping():
    print("waiting for result before ping...")
    result = await sleep(5)
    print(f"result: {result}")
    while True:
        print("ping")
        time.sleep(1)
        # yield control to the event loop. We cannot use (yield in a "true" coroutine)
        await sleep(0)


async def pong():
    while True:
        time.sleep(1)
        await sleep(0)
        print("pong")


if __name__ == "__main__":
    scheduler = Scheduler()
    scheduler.create_task(ping())
    scheduler.create_task(pong())
    scheduler.run_forever()
