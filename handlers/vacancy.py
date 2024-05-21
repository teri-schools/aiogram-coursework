from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext

import kb
from db import Repo
from states import Menu, CreateVacancy

vacancy_router = Router()


@vacancy_router.message(F.text == "Ваші вакансії")
async def my_vacancy(message: types.Message, repo: Repo, state: FSMContext):
    vacancy = await repo.paginate_user_vacancies(message.from_user.id, 0)
    await state.set_state(Menu.vacancies)
    if vacancy is None:
        return message.answer(
            "У вас iще немає вакансій.",
            reply_markup=kb.vacancy(),
        )
    return message.answer(
        str(vacancy),
        reply_markup=kb.paginate_buttons(
            "my_vacancies", 0, text="Видалити", data=f"delete_{vacancy.id}"
        ),
    )


@vacancy_router.callback_query(F.data.startswith("my_vacancies_delete_"))
async def delete_vacancy(callback: types.CallbackQuery, repo: Repo, state: FSMContext):
    ident = int(callback.data.removeprefix("my_vacancies_delete_"))
    await repo.delete_vacancy(ident)
    await callback.answer()
    await callback.message.delete()
    await callback.message.answer("Вакансію видалено.", reply_markup=kb.default())


@vacancy_router.callback_query(F.data.startswith("my_vacancies_"))
async def my_vacancies(callback: types.CallbackQuery, repo: Repo, state: FSMContext):
    page = int(callback.data.removeprefix("my_vacancies_"))
    if page < 0:
        return callback.answer("Це перша сторінка.", show_alert=True)
    vacancy = await repo.paginate_user_vacancies(callback.from_user.id, page)
    if vacancy is None:
        return callback.answer("Це остання сторінка.", show_alert=True)
    await callback.answer()
    await callback.message.edit_text(
        str(vacancy),
        reply_markup=kb.paginate_buttons(
            "my_vacancies", page, text="Видалити", data=f"delete_{vacancy.id}"
        ),
    )


@vacancy_router.message(Menu.vacancies, F.text == "Створити вакансію")
async def create_vacancy(message: types.Message, state: FSMContext):
    await state.set_state(CreateVacancy.title)
    await message.answer("Введіть назву вакансії.", reply_markup=kb.default())


@vacancy_router.message(CreateVacancy.title)
async def create_vacancy_title(message: types.Message, state: FSMContext):
    await state.update_data(title=message.text)
    await state.set_state(CreateVacancy.description)
    await message.answer("Введіть опис вакансії.", reply_markup=kb.default())


@vacancy_router.message(CreateVacancy.description)
async def create_vacancy_description(message: types.Message, state: FSMContext):
    await state.update_data(description=message.text)
    await state.set_state(CreateVacancy.company_name)
    await message.answer("Введіть назву компанії.", reply_markup=kb.default())


@vacancy_router.message(CreateVacancy.company_name)
async def create_vacancy_company_name(message: types.Message, state: FSMContext):
    await state.update_data(company_name=message.text)
    await state.set_state(CreateVacancy.location)
    await message.answer("Введіть місце розташування.", reply_markup=kb.default())


@vacancy_router.message(CreateVacancy.location)
async def create_vacancy_location(message: types.Message, state: FSMContext):
    await state.update_data(location=message.text)
    await state.set_state(CreateVacancy.salary)
    await message.answer("Введіть заробітну плату.", reply_markup=kb.default())


@vacancy_router.message(CreateVacancy.salary)
async def create_vacancy_salary(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        return message.answer(
            "Будь ласка, введіть коректне числове значення для заробітної плати.",
            reply_markup=kb.default(),
        )
    await state.update_data(salary=int(message.text))
    await state.set_state(CreateVacancy.skills)
    return message.answer("Ведіть навички для вакансії.", reply_markup=kb.wait_finish())


@vacancy_router.message(CreateVacancy.skills, F.text == "Завершити")
async def finish_create_vacancy(message: types.Message, repo: Repo, state: FSMContext):
    data = await state.get_data()
    await state.clear()

    await repo.add_vacancy(message.from_user.id, data)

    await message.answer(
        f"Вакансія \"{data['title']}\" створена успішно!", reply_markup=kb.main()
    )


@vacancy_router.message(CreateVacancy.skills)
async def create_vacancy_add_skills(message: types.Message, state: FSMContext):
    data = await state.get_data()
    skills = data.get("skills", [])
    skills.append(message.text)
    await state.update_data(skills=skills)
