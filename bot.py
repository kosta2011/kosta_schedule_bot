import yaml
import datetime
import os
from telegram import Bot
import asyncio

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
SCHEDULE_FILE = "schedule.yaml"

def load_schedule(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return yaml.safe_load(file)['trainings']

def get_today_training(schedule):
    today = datetime.date.today()
    weekday_today = today.strftime("%A")
    date_today_str = today.strftime('%Y-%m-%d')

    for training in schedule:
        if training['date'] == date_today_str:
            return training

    past_trainings = [
        t for t in schedule
        if t['weekday'] == weekday_today and datetime.datetime.strptime(t['date'], '%Y-%m-%d').date() < today
    ]

    if past_trainings:
        return sorted(past_trainings, key=lambda x: x['date'], reverse=True)[0]

    return None

async def send_training():
    schedule = load_schedule(SCHEDULE_FILE)
    training = get_today_training(schedule)

    if training:
        message = f"📌 Тренировки на {training['weekday']} ({training['date']}):\n"
        message += "\n".join(f"- {exercise}" for exercise in training['exercises'])
    else:
        message = "🚫 Сегодня тренировок нет."

    bot = Bot(token=TOKEN)
    await bot.send_message(chat_id=CHAT_ID, text=message)

if __name__ == "__main__":
    asyncio.run(send_training())


