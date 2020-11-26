from pyrogram import Client
import json
from os import path
from warnings import warn
from apscheduler.schedulers.background import BackgroundScheduler


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Bot(metaclass=Singleton):

    def __init__(self):
        self.settings = {}
        self.pending = {}
        self.scheduler = BackgroundScheduler()
        self.scheduler.start()
        account_name, bot_token, plugins = self.load()
        self.client = Client(account_name, bot_token=bot_token,
                             plugins=plugins)

    def load(self) -> list:
        if path.exists('settings.json'):
            with open('settings.json', 'r', encoding='utf-8') as file:
                self.settings = json.load(file)
        else:
            raise AssertionError(
                "You should have a settings.json file first. Use the template "
                "'settings.json.example' and add your bot token.")
        if 'admins' not in self.settings or len(self.settings['admins']) == 0:
            warn("There's no admin for this bot. Set some admin to use this bot correctly.")
            self.settings['admins'] = []
        if 'disclaimer' not in self.settings:
            warn("There's no disclaimer for this bot. Set a disclaimer to use this bot correctly.")
            self.settings['disclaimer'] = "UNSET"
        return [self.settings['account_name'] if 'account_name' in self.settings else 'my_account',
                self.settings['bot_token'] if 'bot_token' in self.settings else None,
                self.settings['plugins'] if 'plugins' in self.settings else None]

    def admin(self, user_id) -> bool:
        return str(user_id) in self.settings['admins']

    def run(self):
        with self.client as client:
            if 'my_username' not in self.settings:
                self.settings['my_username'] = client.get_me().username
        self.client.run()


bot = Bot()
if __name__ == "__main__":
    bot.run()
