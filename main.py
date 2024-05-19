import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from config import TOKEN
from models import Person, Kavun
from states import CreatePerson, CreateKavun

dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!")


@dp.message(F.text == "create Person")
async def create_person(message: Message, state: FSMContext) -> None:
    await state.set_state(CreatePerson.input_name)
    await message.reply("Enter name: ")


@dp.message(F.text == "create Kavun")
async def create_kavun(message: Message, state: FSMContext):
    await state.set_state(CreateKavun.input_weight)
    await message.reply("Enter weight: ")


@dp.message(F.text, CreatePerson.input_name)
async def echo_handler(message: Message, state: FSMContext) -> None:
    person = Person()
    person.set_name(message.text)
    await message.answer(f"Person created: {person.info()}")
    await state.clear()


@dp.message(F.text, CreateKavun.input_weight)
async def echo_handler(message: Message, state: FSMContext):
    try:
        weight = float(message.text)
    except ValueError:
        return message.answer("Invalid weight. Please enter a number.")

    kavun = Kavun()
    kavun.set_weight(weight)
    await message.answer(f"Kavun created: {kavun.info()}")
    await state.clear()


@dp.message()
async def understand(message: Message):
    await message.answer("I don't understand. Try 'create Person' or 'create Kavun'.")




if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp.run_polling(bot)
