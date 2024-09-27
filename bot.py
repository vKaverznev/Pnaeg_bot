from flask import Flask, request
import telegram
import os

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
    bot.set_webhook(url=WEBHOOK_URL)
    print(f"Вебхук установлен на {WEBHOOK_URL}")
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
