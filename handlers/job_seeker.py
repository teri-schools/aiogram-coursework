from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext

import kb
from db import Repo
from states import Menu, CreateJobSeeker
from utils import get_job_seeker_report

job_seeker_router = Router()


@job_seeker_router.message(F.text == "Профіль кандитата")
async def job_seeker(message: types.Message, repo: Repo, state: FSMContext):
    user = await repo.get_user(message.from_user.id)
    if user.job_seeker_id is None:
        await state.set_state(Menu.create_job_seeker)
        return await message.answer(
            "У вас неммає профілю кандидата, хочете його створити?",
            reply_markup=kb.create_job_seeker(),
        )
    job_seeker = await repo.get_jobseeker(user.job_seeker_id)
    await message.answer(
        get_job_seeker_report(job_seeker), reply_markup=kb.exists_job_seeker()
    )


@job_seeker_router.message(F.text == "Видалити профіль кандитата")
async def del_job_seeker(message: types.Message, repo: Repo, state: FSMContext):
    user = await repo.get_user(message.from_user.id)
    await repo.delete_jobseeker(user.job_seeker_id)
    await message.answer("Профіль було видалено", reply_markup=kb.default())


@job_seeker_router.message(Menu.create_job_seeker)
async def create_job_seeker(message: types.Message, state: FSMContext):
    await state.set_state(CreateJobSeeker.first_name)
    await message.answer("Введіть своє ім'я", reply_markup=kb.default())


@job_seeker_router.message(CreateJobSeeker.first_name)
async def create_job_seeker_first_name(message: types.Message, state: FSMContext):
    await state.update_data(first_name=message.text)
    await state.set_state(CreateJobSeeker.last_name)
    await message.answer("Введіть своє прізвище", reply_markup=kb.default())


@job_seeker_router.message(CreateJobSeeker.last_name)
async def create_job_seeker_last_name(message: types.Message, state: FSMContext):
    await state.update_data(last_name=message.text)
    await state.set_state(CreateJobSeeker.middle_name)
    await message.answer("Введіть по-батькові.", reply_markup=kb.default())


@job_seeker_router.message(CreateJobSeeker.middle_name)
async def create_job_seeker_middle_name(message: types.Message, state: FSMContext):
    await state.update_data(middle_name=message.text)
    await state.set_state(CreateJobSeeker.email)
    await message.answer("Введіть свою електронну адресу", reply_markup=kb.default())


@job_seeker_router.message(CreateJobSeeker.email)
async def create_job_seeker_email(message: types.Message, state: FSMContext):
    await state.update_data(email=message.text)
    await state.set_state(CreateJobSeeker.phone_number)
    await message.answer("Введіть свій номер телефону", reply_markup=kb.send_phone())


@job_seeker_router.message(F.text, CreateJobSeeker.phone_number)
async def create_job_seeker_phone_number(message: types.Message, state: FSMContext):
    await state.update_data(phone_number=message.text)
    await state.set_state(CreateJobSeeker.experience)
    await message.answer(
        "Введіть ваш досвід роботи(В роках)", reply_markup=kb.default()
    )


@job_seeker_router.message(F.contact.phone_number, CreateJobSeeker.phone_number)
async def create_job_seeker_phone_number(message: types.Message, state: FSMContext):
    await state.update_data(phone_number=message.contact.phone_number)
    await state.set_state(CreateJobSeeker.experience)
    await message.answer(
        "Введіть ваш досвід роботи(В роках)", reply_markup=kb.default()
    )


@job_seeker_router.message(CreateJobSeeker.experience)
async def create_job_seeker_experience(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        return await message.answer("Досвід має бути в роках, одним числом.")
    await state.update_data(experience=int(message.text), skills=[])
    await state.set_state(CreateJobSeeker.skills)
    await message.answer("Введіть ваші навики(skill)", reply_markup=kb.wait_finish())


@job_seeker_router.message(CreateJobSeeker.skills, F.text == "Завершити")
async def finish_create_job_seeker(
    message: types.Message, repo: Repo, state: FSMContext
):
    data = await state.get_data()
    await state.clear()

    await repo.add_jobseeker(message.from_user.id, data)

    await message.answer(get_job_seeker_report(data))
    await message.answer(
        "Ваш профіль кандидата на роботу створено!", reply_markup=kb.main()
    )


@job_seeker_router.message(CreateJobSeeker.skills)
async def create_job_seeker_add_skills(message: types.Message, state: FSMContext):
    data = await state.get_data()
    skills = data.get("skills", [])
    skills.append(message.text)
    await state.update_data(skills=skills)
