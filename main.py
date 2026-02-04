import asyncio
import datetime
import os
import random
from enum import StrEnum

from aiogram import Bot, Dispatcher, Router, F
from aiogram.filters import CommandStart
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

bot = Bot(token=os.environ.get("BOT_TOKEN"))

router = Router()

local_storage = {}
texts = {
    "start_day_tracking": "✅Start day tracking",
    "stop_day_tracking": "❌Stop day tracking",
    "check_in": "I did Warmup!",
}
praise_words = [
    "well done",
    "great job",
    "excellent",
    "awesome",
    "nice work",
    "good job",
    "brilliant",
    "fantastic",
    "amazing",
    "perfect",
    "outstanding",
    "impressive",
    "way to go",
    "keep it up",
    "you nailed it",
    "superb",
    "remarkable",
    "splendid",
    "top-notch",
    "kudos",
]
start_button_kb = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text=texts["start_day_tracking"])]]
)

check_in_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=texts["stop_day_tracking"])],
        [KeyboardButton(text=texts["check_in"])],
    ],
    resize_keyboard=True,
)


class FSMEyeChecker(StrEnum):
    day_pending = 'day_pending'
    wait_to_check = 'wait_to_check'

    day_stop = 'day_stop'


@router.message(CommandStart())
async def handle_start(message: Message):
    await message.reply(text="Working!", reply_markup=start_button_kb)


@router.message(F.text == texts["start_day_tracking"])
async def handle_day_start(message: Message):
    await message.reply(text="Okay! You start your work day!", reply_markup=ReplyKeyboardRemove())
    chat_id = message.chat.id
    local_storage[chat_id] = {
        "current_state": FSMEyeChecker.day_pending,
        "start_date_tracking": datetime.datetime.now()
    }


async def start_broadcast():
    while True:
        to_remove_chat_ids = set()
        for chat_id, user_info in local_storage.items():
            state = user_info['current_state']

            if state == FSMEyeChecker.day_stop:
                to_remove_chat_ids.add(chat_id)
                continue

            ignored_time = datetime.datetime.now() - user_info['start_date_tracking']

            if ignored_time.seconds > 21 * 60 and state != FSMEyeChecker.wait_to_check:
                await bot.send_message(
                    chat_id=chat_id,
                    text="Stand up! And do some warmup!",
                    reply_markup=check_in_kb,
                )
                local_storage[chat_id]['current_state'] = FSMEyeChecker.wait_to_check
                continue

            elif ignored_time.seconds > 21 * 60 and state == FSMEyeChecker.wait_to_check:

                if (ignored_time.seconds - (21 * 60)) % 60 == 0:
                    await bot.send_message(
                        chat_id=chat_id,
                        text="Stand up! And do some warmup!",
                        reply_markup=check_in_kb,
                    )

        for chat_id in to_remove_chat_ids:
            del local_storage[chat_id]
        await asyncio.sleep(0.1)


@router.message(F.text == texts["stop_day_tracking"])
async def handle_day_stop(message: Message):
    local_storage[message.chat.id]['current_state'] = FSMEyeChecker.day_stop
    await message.reply(text="You successfully stop your eye tracking", reply_markup=start_button_kb)


@router.message(F.text == texts["check_in"])
async def handle_20_check_in(message: Message):
    local_storage[message.chat.id]['current_state'] = FSMEyeChecker.day_pending
    local_storage[message.chat.id]['start_date_tracking'] = datetime.datetime.now()
    await message.reply(random.choice(praise_words))


async def main():
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)
    dp.include_router(router)

    asyncio.create_task(start_broadcast())

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
