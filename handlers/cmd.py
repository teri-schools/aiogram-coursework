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


@cmd_router.message(Command("set_state"))
async def test(message: types.Message, repo: Repo, state: FSMContext):
    await state.set_state("CreateVacancy:skills")
    await state.set_data(
        {
            "title": "Жуніор пайтон розробник",
            "description": "Треба сосати хуї тимлідам.",
            "company_name": "Помойка",
            "location": "Нахуй",
            "salary": 0,
            "skills": ["пинати хуї", "посилати нах керівництво"],
        }
    )
