from flask import Flask, request
import telegram
import os
from telegram.error import RetryAfter, TelegramError

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
    WEBHOOK_URL = f'https://{HEROKU_APP_NAME}.herokuapp.com/{TOKEN}'
    try:
        # Проверяем, установлен ли вебхук
        webhook_info = bot.get_webhook_info()
        if webhook_info.url != WEBHOOK_URL:
            bot.set_webhook(url=WEBHOOK_URL)
            print(f"Вебхук установлен на {WEBHOOK_URL}")
        else:
            print(f"Вебхук уже установлен на {WEBHOOK_URL}")
    except RetryAfter as e:
        print(f"Превышено ограничение на установку вебхука. Повторите через {e.retry_after} секунд.")
    except TelegramError as e:
        print(f"Ошибка Telegram: {e}")
    except Exception as e:
        print(f"Непредвиденная ошибка: {e}")
else:
    print("Ошибка: Переменная HEROKU_APP_NAME не установлена.")

# Обработчик входящих сообщений от Telegram
@app.route(f'/{TOKEN}', methods=['POST'])
def respond():
    # Получаем обновление от Telegram
    update = telegram.Update.de_json(request.get_json(force=True), bot)

    # Получаем идентификатор чата и текст сообщения
    chat_id = update.message.chat.id
    message = update.message.text

    # Формируем ответ
    response = f"Привет! Это бот для ответов по PNAEG 025. Ваш запрос: {message}"
    bot.send_message(chat_id=chat_id, text=response)

    return 'ok'

# Маршрут для проверки работы приложения
@app.route('/', methods=['GET'])
def index():
    return 'Бот работает!'

# Нет необходимости в блоке if __name__ == "__main__", так как Gunicorn управляет запуском приложения
