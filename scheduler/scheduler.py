from collections import deque
from typing import Generator

from scheduler.future import Future
from scheduler.task import Task
from scheduler.task_protocol import TaskProtocol


class Scheduler:
    def __init__(self):
        self._queue = deque([])

    def create_task(self, coro: Generator):
        task = Task(coro)
        self._schedule(task)

    def _schedule(self, task: TaskProtocol):
        self._queue.append(task)

    def _continue(self, task):
        def callback(result):
            task.val = result
            self._schedule(task)

        return callback

    def run_forever(self):
        while self._queue:
            task = self._queue.pop()
            try:
                future = task.run()
                if isinstance(future, Future):
                    future.add_done_callback(self._continue(task))
                    self._schedule(future)
                else:
                    self._queue.appendleft(task)
            except StopIteration as err:
                print(err.value)
