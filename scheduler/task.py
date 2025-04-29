from typing import Generator
import uuid

from scheduler.future import Future


class Task:
    def __init__(self, coro: Generator):
        self._coro = coro
        self.id = uuid.uuid4()
        self.val = None
        self._stack = []

    def run(self):
        try:
            result = self._coro.send(self.val)
            if isinstance(result, Future):
                return result
            elif isinstance(result, Generator):
                self._stack.append(self._coro)
                self._coro = result
                return self.run()
        except StopIteration as err:
            if self._stack:
                self.val = err.value
                self._coro = self._stack.pop()
                return self.run()
            else:
                raise err
