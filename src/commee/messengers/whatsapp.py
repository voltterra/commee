from collections.abc import Callable

import requests
import uvicorn
from fastapi import FastAPI, Request


class WhatsAppMessenger:
    def __init__(self, token: str, phone_number_id: str, port: int = 5001) -> None:
        self._token = token
        self._phone_number_id = phone_number_id
        self._port = port

    def send_message(self, chat_id: str, text: str) -> None:
        url = API.format(phone_number_id=self._phone_number_id)
        headers = {
            "Authorization": f"Bearer {self._token}",
            "Content-Type": "application/json",
        }
        payload = {
            "messaging_product": "whatsapp",
            "to": chat_id,
            "type": "text",
            "text": {"body": text},
        }
        requests.post(url, headers=headers, json=payload)

    def run(self, on_message: Callable[[str, str], None]) -> None:
        app = FastAPI()

        @app.post("/webhook")
        async def webhook(request: Request):
            body = await request.json()
            try:
                msg = body["entry"][0]["changes"][0]["value"]["messages"][0]
                chat_id = msg["from"]
                text = msg["text"]["body"]
                on_message(chat_id, text)
            except (KeyError, IndexError):
                pass
            return {"status": "ok"}

        uvicorn.run(app, host="0.0.0.0", port=self._port)
