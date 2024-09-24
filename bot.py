from flask import Flask, request
import telegram
import os

# Инициализация Flask
app = Flask(__name__)

# Токен вашего бота
TOKEN = os.getenv("8102277034:AAHPL3s9zgMGGpz3AxR7w3vw-8Zd5pS9_qI")
print(f"TOKEN is: {TOKEN}")
bot = telegram.Bot(token=TOKEN)

@app.route('/{}'.format(TOKEN), methods=['POST'])
def respond():
    # Получаем обновление от Telegram
    update = telegram.Update.de_json(request.get_json(force=True), bot)

    # Получаем чат ID и сообщение пользователя
    chat_id = update.message.chat.id
    message = update.message.text

    # Пример ответа
    response = "Привет! Это бот для ответов по PNAEG 025. Ваш запрос: " + message
    bot.sendMessage(chat_id=chat_id, text=response)

    return 'ok'

@app.route('/', methods=['GET'])
def index():
    return 'Бот работает!'

if __name__ == "__main__":
    app.run(threaded=True)
