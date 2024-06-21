from flask import Flask, request
import requests

app = Flask(__name__)

TELEGRAM_TOKEN = '7383030976:AAF49Fo_8ZpMORFnQqapGtOH-BSKCM7Izyg'
TELEGRAM_API_URL = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/'

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    if 'message' in data:
        chat_id = data['message']['chat']['id']
        send_message(chat_id, 'Нажмите на кнопку ниже, чтобы запустить игру', 'Запустить игру', 'https://itch.io/embed-upload/10665163?color=000000')
    return 'ok'

def send_message(chat_id, text, button_text, button_url):
    url = TELEGRAM_API_URL + 'sendMessage'
    payload = {
        'chat_id': chat_id,
        'text': text,
        'reply_markup': {
            'inline_keyboard': [[{'text': button_text, 'url': button_url}]]
        }
    }
    requests.post(url, json=payload)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
