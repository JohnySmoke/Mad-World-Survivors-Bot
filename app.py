from flask import Flask, request
import requests
import os

app = Flask(__name__)

TELEGRAM_TOKEN = '7383030976:AAF49Fo_8ZpMORFnQqapGtOH-BSKCM7Izyg'
TELEGRAM_API_URL = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/'

@app.route('/')
def index():
    return 'Hello, this is the root URL of the Flask app.'

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    if 'message' in data:
        chat_id = data['message']['chat']['id']
        send_game(chat_id, 'mad_world_survivors')
    return 'ok'

def send_game(chat_id, game_short_name):
    url = TELEGRAM_API_URL + 'sendGame'
    payload = {
        'chat_id': chat_id,
        'game_short_name': game_short_name
    }
    response = requests.post(url, json=payload)
    print(f"Payload: {payload}")  # Для отладки
    print(f"Response: {response.json()}")  # Для отладки

    # Дополнительно, отправьте сообщение с кнопкой запуска игры
    button_url = f"https://t.me/your_bot_username?game={game_short_name}"
    button_payload = {
        'chat_id': chat_id,
        'text': 'Нажмите на кнопку ниже, чтобы запустить игру',
        'reply_markup': {
            'inline_keyboard': [
                [{'text': 'Запустить игру', 'url': button_url}]
            ]
        }
    }
    button_response = requests.post(TELEGRAM_API_URL + 'sendMessage', json=button_payload)
    print(f"Button Payload: {button_payload}")  # Для отладки
    print(f"Button Response: {button_response.json()}")  # Для отладки

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8000))
    app.run(host='0.0.0.0', port=port)
