"""
This module provides utility functions for creating Telegram keyboard markup.

Functions:
    paginate_buttons: Create an inline keyboard for pagination.
    main: Create the main keyboard markup.
    create_job_seeker: Create the keyboard markup for creating a jobseeker profile.
    vacancy: Create the keyboard markup for managing vacancies.
    exists_job_seeker: Create the keyboard markup when a jobseeker profile exists.
    default: Create the default keyboard markup.
    send_phone: Create the keyboard with contact send button
    wait_finish: Create the keyboard markup with a "Finish" button.
    confirm: Create the keyboard markup for confirmation (Yes/No).
"""
from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)


def paginate_buttons(prefix: str, page: int, text: str = None, data: str = None):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="<", callback_data=f"{prefix}_{page - 1}"),
                InlineKeyboardButton(text=">", callback_data=f"{prefix}_{page + 1}"),
            ],
            (
                [InlineKeyboardButton(text=text, callback_data=f"{prefix}_{data}")]
                if text and data
                else []
            ),
        ]
    )


def main():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="Профіль кандитата"),
                KeyboardButton(text="Найти вакансію"),
            ],
            [
                KeyboardButton(text="Ваші вакансії"),
                KeyboardButton(text="Найти кандидатів"),
            ],
        ],
        resize_keyboard=True,
    )


def create_job_seeker():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Створити профіль кандитата")],
            [KeyboardButton(text="До меню")],
        ],
        resize_keyboard=True,
    )


def vacancy():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Створити вакансію")],
            [KeyboardButton(text="До меню")],
        ],
        resize_keyboard=True,
    )


def exists_job_seeker():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Видалити профіль кандитата")],
            [KeyboardButton(text="До меню")],
        ],
        resize_keyboard=True,
    )


def default():
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="До меню")]], resize_keyboard=True
    )


def send_phone():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Мій номер", request_contact=True)],
            [KeyboardButton(text="До меню")],
        ],
        resize_keyboard=True,
    )


def wait_finish():
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Завершити")], [KeyboardButton(text="До меню")]],
        resize_keyboard=True,
    )


def confirm():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Ні"), KeyboardButton(text="Так")],
            [KeyboardButton(text="До меню")],
        ],
        resize_keyboard=True,
    )
