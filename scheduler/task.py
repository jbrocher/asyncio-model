from typing import Coroutine
import uuid


class Task:
    def __init__(self, coro: Coroutine):
        self._coro = coro
        self.id = uuid.uuid4()
        self.val = None

    def run(self):
        return self._coro.send(self.val)
