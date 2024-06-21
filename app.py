from flask import Flask, request
import requests
import os

app = Flask(__name__)

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN', '7383030976:AAF49Fo_8ZpMORFnQqapGtOH-BSKCM7Izyg')
TELEGRAM_BOT_USERNAME = os.getenv('TELEGRAM_BOT_USERNAME', 'mad_world_survivors_bot')
TELEGRAM_API_URL = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/'

@app.route('/')
def index():
    return 'Hello, this is the root URL of the Flask app.'

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    print(f"Webhook received: {data}")  # Отладка: вывод полученных данных
    if 'message' in data:
        chat_id = data['message']['chat']['id']
        send_game(chat_id, 'mad_world_survivors')
    elif 'callback_query' in data:
        handle_callback_query(data['callback_query'])
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

def handle_callback_query(callback_query):
    try:
        query_id = callback_query['id']
        chat_id = callback_query['message']['chat']['id']
        game_short_name = callback_query['game_short_name']
        url = TELEGRAM_API_URL + 'answerCallbackQuery'
        # Убедитесь, что TELEGRAM_BOT_USERNAME установлен правильно
        if TELEGRAM_BOT_USERNAME is None or TELEGRAM_BOT_USERNAME == '':
            raise ValueError("TELEGRAM_BOT_USERNAME is not set correctly.")
        payload = {
            'callback_query_id': query_id,
            'url': "https://itch.io/embed-upload/10665163?color=000000"
        }
        response = requests.post(url, json=payload)
        print(f"Callback Payload: {payload}")  # Для отладки
        print(f"Callback Response: {response.json()}")  # Для отладки
    except KeyError as e:
        print(f"KeyError: {e}")  # Для отладки
    except Exception as e:
        print(f"Exception: {e}")  # Для отладки

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8000))
    app.run(host='0.0.0.0', port=port)
