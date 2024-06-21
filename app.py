from flask import Flask, request
import requests
import os

app = Flask(__name__)

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN', '7383030976:AAF49Fo_8ZpMORFnQqapGtOH-BSKCM7Izyg')
TELEGRAM_API_URL = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/'

@app.route('/')
def index():
    return 'Hello, this is the root URL of the Flask app.'

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    if 'message' in data:
        chat_id = data['message']['chat']['id']
        send_inline_button(chat_id, 'Запустить игру', 'https://itch.io/embed-upload/10665163?color=000000')
    return 'ok'

def send_inline_button(chat_id, text, url):
    url_button = f"url={url}"
    payload = {
        'inline_keyboard': [
            [{'text': text, 'url_button': url_button}]
        ]
    }
    requests.post(TELEGRAM_API_URL, json=payload)
