"""
This module contains handlers for processing commands in a Telegram bot.

Functions:
    wellcome: Handles the /start command, greets the user and presents the main menu.
    go_to_menu: Returns the user to the main menu from any state.
    test: A test function for debugging purposes.
    set_state: A test function for setting the state and data in the FSM context.
"""
from aiogram import Router, types, F
from aiogram.filters import CommandStart, StateFilter, Command
from aiogram.fsm.context import FSMContext

import kb
from db import Repo

cmd_router = Router()


@cmd_router.message(CommandStart())
async def wellcome(message: types.Message, repo: Repo):
    user = await repo.get_user(message.from_user.id)
    if user:
        return message.answer("З поверненням.", reply_markup=kb.main())
    await repo.add_user(message.from_user.id)
    await message.reply(
        "Доброго дня. Цей бот надасть вам можливості найти хорошу вакансію, або найти хороших кандидатів.",
        reply_markup=kb.main(),
    )


@cmd_router.message(F.text == "До меню", StateFilter("*"))
async def go_to_menu(message: types.Message):
    await message.answer("Виберіть опцію для взаємодії", reply_markup=kb.main())


@cmd_router.message(Command("test"))
async def test(message: types.Message, repo: Repo, state: FSMContext):
    return message.answer(
        f"User: {await repo.get_user(message.from_user.id)}\nState: {await state.get_state()}\nData: {await state.get_data()}"
    )