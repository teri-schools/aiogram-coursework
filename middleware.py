from typing import Callable, Dict, Any, Awaitable

from aiogram.fsm.middleware import BaseMiddleware
from aiogram.types import TelegramObject
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from db import Repo


class DatabaseMiddleware(BaseMiddleware):
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
