"""
This module contains handlers for searching and paginating job vacancies.

Functions:
    search_vacencies: Displays the first page of job vacancies.
    responded_vacency: Handles the user's response to a job vacancy.
    search_vacencies: Handles pagination of job vacancies.
"""
from aiogram import Router, types, F, Bot
from aiogram.fsm.context import FSMContext

import kb
from db import Repo
from utils import get_job_seeker_report

search_vacencies_router = Router()


@search_vacencies_router.message(F.text == "Найти вакансію")
async def search_vacencies(message: types.Message, repo: Repo, state: FSMContext):
    vacency = await repo.paginate_vacencies(0)
    if vacency is None:
        return message.answer("Не знайдено жодної вакансії.")
    return message.answer(
        str(vacency),
        reply_markup=kb.paginate_buttons(
            "search_vacencies", 0, text="Відгукнутися", data=f"responded_{vacency.id}"
        ),
    )


@search_vacencies_router.callback_query(
    F.data.startswith("search_vacencies_responded_")
)
async def responded_vacency(
    callback: types.CallbackQuery, repo: Repo, state: FSMContext, bot: Bot
):
    ident = int(callback.data.removeprefix("search_vacencies_responded_"))
    user = await repo.get_user(callback.from_user.id)
    if user.job_seeker_id is None:
        return callback.answer("У вас немає профіля кандидата.", show_alert=True)
    jobseeker = await repo.get_jobseeker(user.job_seeker_id)
    vacency = await repo.get_vacancy(ident)
    owner_id = await repo.get_vacancy_user_id(ident)
    await bot.send_message(
        owner_id,
        f'Відгук на вакансію "{vacency.title}"\n\n' + get_job_seeker_report(jobseeker),
    )
    await callback.answer("Відгук успішно доставлений.", show_alert=True)


@search_vacencies_router.callback_query(F.data.startswith("search_vacencies_"))
async def search_vacencies(
    callback: types.CallbackQuery, repo: Repo, state: FSMContext
):
    page = int(callback.data.removeprefix("search_vacencies_"))
    if page < 0:
        return callback.answer("Це перша сторінка.", show_alert=True)
    vacency = await repo.paginate_vacencies(page)
    if vacency is None:
        return callback.answer("Це остання сторінка.", show_alert=True)
    await callback.answer()
    await callback.message.edit_text(
        str(vacency),
        reply_markup=kb.paginate_buttons(
            "search_vacencies",
            page,
            text="Відгукнутися",
            data=f"responded_{vacency.id}",
        ),
    )
