import asyncio
import os
from aiogram import Bot, Dispatcher
from config_reader import config
from handlers.handlers import *
from handlers.handlers import router
from redisdb import *
from scheldule import *
import aiocron
import random
import logging

# Запуск бота

@aiocron.crontab("05 13 * * 2")
async def poll_daily_broadcast():
    await start_poll()
@aiocron.crontab("00 15 * * 3")
async def pair_daily_broadcast():
    await create_pairs()
@aiocron.crontab("25 14 * * 1-5")
async def schedule_daily_broadcast():
    await send_message_to_subscribers()
BOT_TOKEN = os.getenv("BOT_TOKEN")
logging.basicConfig(logging.DEBUG)
bot = Bot(token=BOT_TOKEN , parse_mode='HTML')
dp = Dispatcher()
dp.include_router(router)
# Альтернативный вариант регистрации роутеров по одному на строку
# dp.include_router(questions.router)
# dp.include_router(different_types.router)
chat_id = 921953226 #личный ччат со мной можно заменить на свой
# время запуска опроса
async def start_poll():
    markup = ReplyKeyboardRemove()
    poll_text = "Всем привет✌🏻, в эфире наша еженедельная программа по наработке социального капитала!🥳 Примешь участие в нашем празднике жизни? ☺️🎉(Досрочно завершить голосование /pairs)"
    options = ["✅ Да", "❌ Нет, в другой раз"]
    await bot.send_poll(
        chat_id=chat_id,
        question=poll_text,
        options=options,
        is_anonymous=False,  # Устанавливает опрос как неанонимный
        reply_markup=markup
    )
async def send_message_to_subscribers():
    text = send_schedule()
    subscribers = await load_list_from_redis(redis_url, key = 'chats')
    for subscriber in subscribers:
        await bot.send_message(subscriber, text)
#разделение по парам или тройкам
async def create_pairs():
    yes_users = await load_dict_from_redis(redis_url, key = chat_id)
    if not yes_users:
        await bot.send_message(chat_id, "Нет активных опросов.")
        return
    poll_id = list(yes_users.keys())[-1]  # Получаем последний опрос
    users = yes_users[poll_id]
    
    if len(users) < 2:
        await bot.send_message(chat_id, "Недостаточно участников для создания пар.")
        return
    pair_text = f"На этой неделе за 🧀 и 🍷 встретятся:\n\n"
    while len(users)>=2:
            pair = random.sample(users, 2)
            pair_text += f"• {' и '.join(['@' + username for username in pair])}\n"
            users = [user for user in users if user not in pair]
            if len(users) == 3:
                    triple = random.sample(users, 3)
                    pair_text += f"• {' и '.join(['@' + username for username in triple])}\n"
    pair_text += "\nДоговоритесь об удобном формате встречи и найдите отклик в сердцах друг друга ❤️!"
    pair_text += "\n\n[DOING LINK](MadeByZealot)"
    await bot.send_message(chat_id, pair_text)
    
# Запускаем бота и пропускаем все накопленные входящие
# Да, этот метод можно вызвать даже если у вас поллинг

dp.start_polling(bot)
    
if __name__ == "__main__":
    asyncio.run()