import logging

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode

from tgbot.config import Config
from tgbot.misc.sheet_amanger import GspreadManager
from tgbot.misc.states import SelectStudies

user_router = Router()


@user_router.message(CommandStart())
async def admin_start(message: Message, dialog_manager: DialogManager, config: Config, sh_manager: GspreadManager):
    data = await sh_manager.get_all_users()
    if f'{message.from_user.id}' in data:
        await message.answer('вы уже записаны на обучение')
        return
    await dialog_manager.start(SelectStudies.select_city, mode=StartMode.RESET_STACK)
