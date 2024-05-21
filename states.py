from aiogram.fsm.state import StatesGroup, State


class Menu(StatesGroup):
    job_seeker = State()
    create_job_seeker = State()
    vacancies = State()


class CreateJobSeeker(StatesGroup):
    first_name = State()
    last_name = State()
    middle_name = State()

    email = State()
    phone_number = State()

    experience = State()

    skills = State()
    # educations = State()


class CreateVacancy(StatesGroup):
    title = State()
    description = State()
    company_name = State()
    location = State()
    salary = State()

    skills = State()
    # educations = State()
