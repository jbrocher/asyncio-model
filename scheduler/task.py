from typing import Generator
import uuid


class Task:
    def __init__(self, coro: Generator):
        self.id = uuid.uuid4()
        self._coro = coro
        self.val = None

    def run(self):
        self._coro.send(self.val)
