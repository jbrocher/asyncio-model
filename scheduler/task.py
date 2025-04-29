from typing import Generator
import uuid


class Task:
    def __init__(self, coro: Generator):
        self._coro = coro
        self.id = uuid.uuid4()
        self.val = None

    def run(self):
        return self._coro.send(self.val)
