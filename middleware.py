"""
This module defines a middleware for managing database sessions.

Classes:
    DatabaseMiddleware: A middleware class that provides a database session and repository instance.
"""
from typing import Callable, Dict, Any, Awaitable

from aiogram.fsm.middleware import BaseMiddleware
from aiogram.types import TelegramObject
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from db import Repo


class DatabaseMiddleware(BaseMiddleware):
    """
    A middleware class that provides a database session and repository instance.

    This middleware ensures that a new database session and repository instance are created
    for each incoming update, and the session is closed after the update is processed.
    """
    def __init__(self, sessionmake: sessionmaker[AsyncSession]):
        self.sessionmake = sessionmake

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        async with self.sessionmake() as session:
            data["db"] = session
            data["repo"] = Repo(session)
            return await handler(event, data)
