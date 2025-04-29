from abc import abstractmethod
from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from scheduler.future import Future


class TaskProtocol(Protocol):
    @abstractmethod
    def run(self) -> "Future | None": ...
