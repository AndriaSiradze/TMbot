import logging
from typing import Any

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, StartMode

from tgbot.misc.states import QuestionAnswer


async def on_select_city(c:CallbackQuery, widget:Any, dialog_manager:DialogManager, item: str):
    ctx = dialog_manager.current_context()
    ctx.dialog_data['city'] = item
    await dialog_manager.next()

async def on_select_date(c:CallbackQuery, widget:Any, dialog_manager:DialogManager, item: str):
    ctx = dialog_manager.current_context()
    await dialog_manager.start(QuestionAnswer.name,
                               data={
                                   'city': ctx.dialog_data['city'],
                                   'date': item
                               },
                               mode=StartMode.RESET_STACK)