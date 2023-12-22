from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, PollAnswer, ReplyKeyboardRemove
from redisdb import *
from scheldule import *

router = Router()  # [1]

chats = []
yes_users = {}


@router.message(Command("start"))  # [2]
async def cmd_start(message: Message):
    new_chat = message.chat.id
    chats.append(new_chat)
    await save_list_to_redis(redis_url, key = 'chats', my_list = chats)
    await message.answer(
        "Привет, это DoingLink!🔥🔥🔥\n Я умею отправлять события из вашего Google Calendar 📅(/schedule(на сегодня), /mycal(ближайшие 10))\n создавать RandomCoffee(/go) ☕️ , а также поздравлять с днем рождения!🥳",
        reply_markup=get_yes_no_kb()
    )

@router.message(Command('myid'))
async def myid(message: Message):
    new_chat = message.chat.id
    await message.answer(new_chat)

@router.message(Command('mycal'))
async def mycal(message: Message):
    cal = get_schedule_data()
    await message.answer(f"Ваши ближайшие события:\n "f"{cal}")


@router.poll()
async def poll_answer(poll_answer: PollAnswer):
    user = poll_answer.User
    username = user.username
    poll_id = poll_answer.poll_id
    chat_id = poll_answer.chat.id
    key = chat_id
    # Проверяем, что опрос с таким poll_id существует и ответ "Да"
    if  poll_answer.option_ids[0] == 0:
        yes_users[poll_id].append(username)
        await save_dict_to_redis(redis_url, key, yes_users)