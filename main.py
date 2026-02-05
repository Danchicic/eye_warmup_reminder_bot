import asyncio
import os
import random

from aiogram import Bot, Dispatcher, Router, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

storage = MemoryStorage()
dp = Dispatcher(storage=storage)
bot = Bot(token=os.environ.get("BOT_TOKEN"))

router = Router()
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


class FSMEyeChecker(StatesGroup):
    day_pending = State()
    wait_to_check = State()

    day_stop = State()


@router.message(CommandStart())
async def handle_start(message: Message):
    await message.reply(text="Working!", reply_markup=start_button_kb)


@router.message(F.text == texts["start_day_tracking"])
async def handle_day_start(message: Message, state: FSMContext):
    await message.reply(text="Okay! You start your work day!", reply_markup=ReplyKeyboardRemove())
    await state.set_state(FSMEyeChecker.day_pending)
    chat_id = message.chat.id
    while True:
        if (await state.get_state()) == FSMEyeChecker.day_stop:
            break

        if (await state.get_state()) == FSMEyeChecker.wait_to_check:
            await asyncio.sleep(60)

            if (await state.get_state()) == FSMEyeChecker.day_stop:
                break

            if (await state.get_state()) == FSMEyeChecker.day_pending:
                continue

            await bot.send_message(
                chat_id=chat_id,
                text="Stand up! And do some warmup!",
                reply_markup=check_in_kb,
            )
        else:
            await asyncio.sleep(60 * 21)

            if (await state.get_state()) == FSMEyeChecker.day_stop:
                break

            await bot.send_message(
                chat_id=chat_id,
                text="Stand up! And do some warmup!",
                reply_markup=check_in_kb,
            )
            await state.set_state(FSMEyeChecker.wait_to_check)


@router.message(F.text == texts["stop_day_tracking"])
async def handle_day_stop(message: Message, state: FSMContext):
    await state.set_state(FSMEyeChecker.day_stop)
    await message.reply(text="You successfully stop your eye tracking", reply_markup=start_button_kb)


@router.message(F.text == texts["check_in"])
async def handle_20_check_in(message: Message, state: FSMContext):
    await state.set_state(FSMEyeChecker.day_pending)

    await message.reply(random.choice(praise_words))


dp.include_router(router)
if __name__ == "__main__":
    asyncio.run(dp.start_polling(bot))
