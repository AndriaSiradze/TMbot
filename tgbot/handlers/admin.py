from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram_dialog import DialogManager

from tgbot.filters.admin import AdminFilter
from tgbot.misc.states import SelectStudies

admin_router = Router()
admin_router.message.filter(AdminFilter())


@admin_router.message(CommandStart())
async def admin_start(message: Message, dialog_manager:DialogManager):
    await dialog_manager.start(SelectStudies.select_date)

