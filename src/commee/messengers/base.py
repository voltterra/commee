from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import Dict


class AbstractMessenger(ABC):
    @abstractmethod
    def send_message(self, chat_id: str, text: str) -> None: ...

    @abstractmethod
    def run(self, on_message: Callable[[str, str], None]) -> None: ...

    @abstractmethod
    def receive_message(self, offset: int) -> Dict: ...
