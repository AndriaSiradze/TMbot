from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message


class ConfigMiddleware(BaseMiddleware):
    def __init__(self, config, sheet_manager) -> None:
        self.config = config
        self.sh_manager = sheet_manager

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        data["config"] = self.config
        data["sh_manager"] = self.sh_manager
        return await handler(event, data)

