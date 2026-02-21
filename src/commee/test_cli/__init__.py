import os

import click
from dotenv import load_dotenv

from commee.messengers.telegram import TelegramMessenger
from commee.messengers.whatsapp import WhatsAppMessenger

load_dotenv()


@click.group()
def cli():
    pass


@cli.command("tg")
@click.argument("message")
def run_tg(message: str):
    app = TelegramMessenger(os.getenv("TG_APP_TOKEN", ""))
    chat_id = os.getenv("TG_CHAT_ID", "")
    app.send_message(chat_id, message)
    app.run(lambda cid, text: print(f"[{cid}]: {text}"))


@cli.command("wa")
@click.argument("message")
def run_wa(message: str):
    app = WhatsAppMessenger(
        token=os.getenv("WA_TOKEN", ""),
        phone_number_id=os.getenv("WA_PHONE_NUMBER_ID", ""),
    )
    chat_id = os.getenv("WA_CHAT_ID", "")
    app.send_message(chat_id, message)
    app.run(lambda cid, text: print(f"[{cid}]: {text}"))


if __name__ == "__main__":
    cli()
