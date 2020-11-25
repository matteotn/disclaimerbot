from pyrogram import Client


class Bot:

    def __init__(self, bot_token, account_name="my_account", plugins_folder='plugins'):
        plugins = {
            'root': f"{plugins_folder}"
        }
        self.client = Client(account_name, bot_token=bot_token, plugins=plugins)

    def run(self):
        self.client.run()


