from flask import Flask, request
import telegram
import os
import json

# Инициализация Flask-приложения
app = Flask(__name__)

# Получение токена бота из переменных окружения
TOKEN = os.getenv("TOKEN")
if TOKEN is None:
    print("Ошибка: Переменная TOKEN не установлена.")
else:
    print("Переменная TOKEN успешно получена.")

# Инициализация бота Telegram
bot = telegram.Bot(token=TOKEN)

# Установка вебхука
HEROKU_APP_NAME = os.getenv("HEROKU_APP_NAME")
if HEROKU_APP_NAME:
    WEBHOOK_URL = f'https://{HEROKU_APP_NAME}.herokuapp.com/'
    try:
        # Проверяем, установлен ли вебхук на нужный URL
        webhook_info = bot.get_webhook_info()
        if webhook_info.url != WEBHOOK_URL:
            bot.set_webhook(url=WEBHOOK_URL)
            print(f"Вебхук установлен на {WEBHOOK_URL}")
        else:
            print(f"Вебхук уже установлен на {WEBHOOK_URL}")
    except Exception as e:
        print(f"Ошибка при установке вебхука: {e}")
else:
    print("Ошибка: Переменная HEROKU_APP_NAME не установлена.")

# Обработчик входящих сообщений от Telegram
@app.route('/', methods=['GET', 'POST'])
def respond():
    if request.method == 'POST':
        try:
            json_string = request.get_data().decode('utf-8')
            print(f"Получен POST-запрос: {json_string}")
            update = telegram.Update.de_json(json.loads(json_string), bot)
            # Проверяем наличие сообщения
            if update.message:
                chat_id = update.message.chat.id
                message = update.message.text
                print(f"Сообщение от {chat_id}: {message}")
                # Формируем и отправляем ответ
                response = f"Привет! Это бот для ответов по PNAEG 025. Ваш запрос: {message}"
                bot.send_message(chat_id=chat_id, text=response)
            else:
                print("Нет сообщения в обновлении.")
        except Exception as e:
            print(f"Ошибка при обработке POST-запроса: {e}")
        return 'ok', 200
    else:
        print("Получен GET-запрос")
        return 'Webhook is running!', 200

# Нет необходимости в блоке if __name__ == "__main__", так как Gunicorn управляет запуском приложения

