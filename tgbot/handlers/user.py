import logging

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram_dialog import DialogManager
from gspread_asyncio import AsyncioGspreadWorksheet

from tgbot.config import Config
from tgbot.misc.states import SelectStudies

user_router = Router()


@user_router.message(CommandStart())
async def admin_start(message: Message, dialog_manager:DialogManager,config:Config ):
    agcm = await config.gspread_conf.agcm.authorize()
    sheet = await agcm.open('TMsheet')
    wk: AsyncioGspreadWorksheet = await sheet.get_worksheet(0)
    data = await wk.col_values(8)
    if f'{message.from_user.id}' in data:
        await message.answer('вы уже записаны на обучение')
        return
    logging.info(message.from_user.id)
    logging.info(data)
    logging.info(message.from_user.id in data)
    await dialog_manager.start(SelectStudies.select_city)

