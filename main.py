"""
This module is the entry point of the Telegram bot application.

It sets up the bot, dispatcher, and registers routers and middleware.
"""
import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher

from config import TOKEN
from db import get_async_engine, get_async_sessionmake
from handlers import (
    job_seeker_router,
    cmd_router,
    search_jobseeker_router,
    vacancy_router,
    search_vacencies_router,
)
from middleware import DatabaseMiddleware


# from aiogram.client.default import DefaultBotProperties


async def main():
    """
    The main function that runs the Telegram bot application.
    """
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    logging.info("run main...")

    bot = Bot(token=TOKEN)  # , default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    dp = Dispatcher()
    dp.include_routers(
        cmd_router,
        job_seeker_router,
        search_jobseeker_router,
        vacancy_router,
        search_vacencies_router,
    )

    engine = get_async_engine()
    sessionmake = get_async_sessionmake(engine)
    dp.update.outer_middleware.register(DatabaseMiddleware(sessionmake))

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
