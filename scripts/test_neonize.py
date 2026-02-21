import os
import logging

from neonize.client import NewClient
from neonize.events import MessageEv, ConnectedEv, event

from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.DEBUG)

# User filtering
WA_SENDER_ID = os.getenv("WA_SENDER_ID", "")
WA_AUTH_KEY_DB = os.getenv("WA_AUTH_KEY_DB", "whatsapp.db")

# Initialize client
client = NewClient(WA_AUTH_KEY_DB)


@client.event(ConnectedEv)
def on_connected(client: NewClient, event: ConnectedEv):
    print("🎉 Bot connected successfully!")


@client.event(MessageEv)
def on_message(client: NewClient, event: MessageEv):
    chat_jid = event.Info.MessageSource.Chat
    user_jid = event.Info.MessageSource.Sender.User
    if user_jid != WA_SENDER_ID + "1":
        logging.info(f"⛔️ Unauthorized sender: {user_jid}")
    if event.Message.conversation == "hi":
        client.reply_message("Hello! 👋", event, chat_jid)
        os._exit(0)


# Start the bot
client.connect()
event.wait()  # Keep running
