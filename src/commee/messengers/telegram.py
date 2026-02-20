import time
from collections.abc import Callable
from typing import Dict

import requests

from commee.messengers.base import AbstractMessenger

API = "https://api.telegram.org/bot{token}/{method}"


class TelegramMessenger(AbstractMessenger):
    def __init__(self, token: str) -> None:
        self._token = token

    def _api_url(self, method: str):
        return API.format(token=self._token, method=method)

    def _call(self, method: str, **kwargs):
        return requests.post(self._api_url(method), json=kwargs).json()

    def send_message(self, chat_id: str, text: str) -> None:
        self._call("sendMessage", chat_id=chat_id, text=text)

    def receive_message(self, offset: int) -> Dict:
        return self._call("getUpdates", offset=offset, timeout=30).get("result", [])

    def run(self, on_message: Callable[[str, str], None]) -> None:
        offset = 0
        messages = self.receive_message(offset)
        messages_full = self._call("getUpdates", offset=offset)
        for update in messages:
            offset = update["update_id"] + 1
            msg = update.get("message", {})
            text = msg.get("text")
            chat_id = str(msg.get("chat", {}).get("id", ""))
            if text and chat_id:
                on_message(chat_id, text)
        time.sleep(2)
