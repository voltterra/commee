import os

import click
from dotenv import load_dotenv

from commee.messengers.telegram import TelegramMessenger

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


if __name__ == "__main__":
    cli()
