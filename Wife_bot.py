import telegram
import schedule
import time
import openai
import pytz
from datetime import datetime
import os

# === ПЕРЕМЕННЫЕ ОКРУЖЕНИЯ ===
TOKEN = os.environ.get("8321783290:AAHNCrRvESYiiVq_40S1Dx87ns-bQ6IWGag")  # токен бота из BotFather
CHAT_ID = os.environ.get("-279933760")  # ID жены
OPENAI_API_KEY = os.environ.get("sk-proj-aaj-m1pfQ6YQTwUiw9e1Rj-jYs_vnAs-Gy6FoZRbdrL3KnTrvTgt-YaBDmFZ9CWzx2z-ITxNdbMRT3Blbk-FJ5qt7XxngO-2sWu9-Usbn_sUl51PYJiVhakHkN2WZhNtKFvTWOTz-UmUQvM7IrUkuYbURybqvzQA")  # OpenAI API ключ

TIMEZONE = pytz.timezone("Europe/Moscow")  # московское время

openai.api_key = OPENAI_API_KEY
bot = telegram.Bot(token=TOKEN)

# === ФУНКЦИИ ===
def generate_message(context):
    """
    Генерирует романтичное сообщение через OpenAI
    context: "доброе утро, пожелание дня" или "спокойной ночи, пожелание сладких снов"
    """
    prompt = f"""
    Придумай короткое романтичное сообщение на русском языке на тему "{context}".
    Используй добрый тон, немного юмора и эмодзи.
    Обращайся к жене как 'любимая', 'мой маленький слоненок' или 'моя зая'.
    Сообщение должно быть оригинальным, не длиннее 2-3 предложений.
    """
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.9,
        max_tokens=80
    )
    return response.choices[0].message.content.strip()


def send_good_morning():
    text = generate_message("доброе утро, пожелание хорошего дня")
    bot.send_message(chat_id=CHAT_ID, text=text)
    print(f"[{datetime.now(TIMEZONE).strftime('%H:%M')}] Отправлено утреннее сообщение.")


def send_good_night():
    text = generate_message("спокойной ночи, пожелание сладких снов")
    bot.send_message(chat_id=CHAT_ID, text=text)
    print(f"[{datetime.now(TIMEZONE).strftime('%H:%M')}] Отправлено вечернее сообщение.")


# === РАСПИСАНИЕ ===
schedule.every().day.at("08:00").do(send_good_morning)
schedule.every().day.at("22:00").do(send_good_night)

print("Бот запущен и ждёт времени отправки...")

# === БЕСКОНЕЧНЫЙ ЦИКЛ ===
while True:
    schedule.run_pending()
    time.sleep(60)
