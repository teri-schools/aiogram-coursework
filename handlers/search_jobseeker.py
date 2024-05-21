from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext

import kb
from db import Repo
from utils import get_job_seeker_report

search_jobseeker_router = Router()


@search_jobseeker_router.message(F.text == "Найти кандидатів")
async def search_jobseeker(message: types.Message, repo: Repo, state: FSMContext):
    jobseeker = await repo.paginate_jobseeker(0)
    if jobseeker is None:
        return message.answer("Не знайдено жодного кандидата.")
    return message.answer(
        get_job_seeker_report(jobseeker, True),
        reply_markup=kb.paginate_buttons("search_jobseeker", 0),
    )


@search_jobseeker_router.callback_query(F.data.startswith("search_jobseeker_"))
async def search_jobseeker(
    callback: types.CallbackQuery, repo: Repo, state: FSMContext
):
    page = int(callback.data.removeprefix("search_jobseeker_"))
    print(page)
    if page < 0:
        return callback.answer("Це перша сторінка.", show_alert=True)
    jobseeker = await repo.paginate_jobseeker(page)
    if jobseeker is None:
        return callback.answer("Це остання сторінка.", show_alert=True)
    await callback.answer()
    await callback.message.edit_text(
        get_job_seeker_report(jobseeker, True),
        reply_markup=kb.paginate_buttons("search_jobseeker", page),
    )
