from abc import ABC, abstractmethod
from collections.abc import Callable


class AbstractMessenger(ABC):
    @abstractmethod
    def send_message(self, chat_id: str, text: str) -> None: ...

    @abstractmethod
    def run(self, on_message: Callable[[str, str], None]) -> None: ...
