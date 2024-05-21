"""
This module defines the state machines for jobseeker and vacancy creation.

Classes:
    Menu: A state group for the main menu and related states.
    CreateJobSeeker: A state group for creating a jobseeker profile.
    CreateVacancy: A state group for creating a job vacancy.
"""
from aiogram.fsm.state import StatesGroup, State


class Menu(StatesGroup):
    """
    A state group for the main menu and related states.
    """
    job_seeker = State()
    create_job_seeker = State()
    vacancies = State()


class CreateJobSeeker(StatesGroup):
    """
    A state group for creating a jobseeker profile.
    """
    first_name = State()
    last_name = State()
    middle_name = State()

    email = State()
    phone_number = State()

    experience = State()

    skills = State()
    # educations = State()


class CreateVacancy(StatesGroup):
    """
    A state group for creating a job vacancy.
    """
    title = State()
    description = State()
    company_name = State()
    location = State()
    salary = State()

    skills = State()
    # educations = State()
