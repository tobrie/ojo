import os
import json

from requests import Session

from .utils import get_user_agent


api_url = 'https://api.telegram.org/bot{}/'
chat_id = os.getenv('TG_CHATID')
token = os.getenv('TG_TOKEN')


class Telegram():
    def __init__(self):
        self.s = Session()
        #self.s.headers = {'User-Agent': 'curl/7.67.0'}
        self.s.headers = {'User-Agent': get_user_agent()}

        self.url = api_url.format(token)

    def notify(self, text):
        '''Send telegram message to configured chat.'''
        data = {
            'chat_id': chat_id,
            'text': text
        }
        response = self.s.post(self.url + 'sendMessage', data=data)

        return response.status_code == 200


if __name__ == '__main__':
    t = Telegram()
    if input('send test notification? [Y/n]') != 'n':
        print(t.notify('test'))
