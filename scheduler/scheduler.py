from collections import deque
from typing import Generator

from scheduler.task import Task


class Scheduler:
    def __init__(self):
        self._queue = deque([])

    def create_task(self, coro: Generator):
        task = Task(coro)
        self._queue.append(task)

    def run_forever(self):
        while self._queue:
            task = self._queue.pop()
            try:
                task.run()
                self._queue.appendleft(task)
            except StopIteration as err:
                print(err.value)
