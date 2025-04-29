from abc import ABCMeta, abstractmethod
from datetime import datetime, timedelta, timezone
from typing import Any, Callable

from scheduler.task_protocol import TaskProtocol


class Future(TaskProtocol, metaclass=ABCMeta):
    def __init__(self):
        self._done_callbacks = []
        self.is_done = False
        self._result = None
        self._coro = self._run()

    def __await__(self):
        yield self

    def add_done_callback(self, callback: Callable[[Any], None]):
        self._done_callbacks.append(callback)

    def run(self):
        self._coro.send(None)

    def _run(self):
        while True:
            result = self._check_result()
            if result:
                self._done(result)
                return result
            yield

    def _done(self, result: Any):
        self.is_done = True
        self._result = result
        for callback in self._done_callbacks:
            callback(self._result)

    @abstractmethod
    def _check_result(self) -> Any:
        pass


class Sleep(Future):
    def __init__(self, wait_for: int, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._wait_for = timedelta(seconds=wait_for)
        self._ready_at = datetime.now(tz=timezone.utc) + self._wait_for

    def _check_result(self):
        if datetime.now(tz=timezone.utc) >= self._ready_at:
            return True
