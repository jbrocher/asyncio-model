from abc import ABCMeta, abstractmethod
from datetime import datetime, timedelta, timezone
import selectors
from socket import socket
from typing import Any, Callable

from scheduler.task_protocol import TaskProtocol


class Future(TaskProtocol, metaclass=ABCMeta):
    def __init__(self):
        self._done_callbacks = []
        self.is_done = False
        self._result = None
        self._coro = self._run()

    def __await__(self):
        return (yield self)

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


class AcceptSocket(Future):
    def __init__(self, sock: socket, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._select = selectors.DefaultSelector()
        self._sock = sock
        self._select.register(sock, selectors.EVENT_READ)

    def _check_result(self):
        # Non blocking, return currently ready evens
        events = self._select.select(0)
        if len(events) > 0:
            conn, addr = self._sock.accept()  # Should be ready
            print("accepted", conn, "from", addr)
            conn.setblocking(False)
            return conn


class ReadSocket(Future):
    def __init__(self, sock: socket, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._select = selectors.DefaultSelector()
        self._sock = sock
        self._select.register(sock, selectors.EVENT_READ)

    def _check_result(self):
        # Non blocking, return currently ready evens
        events = self._select.select(0)
        if len(events) > 0:
            data = self._sock.recv(1000)  # Should be ready
            return data
