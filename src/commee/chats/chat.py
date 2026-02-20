from abc import ABC


class AbstractChatSubprocess:
    def __init__(self, chat) -> None:
        pass

    def send_message(self, chat):
        pass

    def create_process(self):

