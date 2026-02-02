import asyncio
import logging
from typing import Any

from aiogram.types import Message, CallbackQuery
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.kbd import Button
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from tgbot.config import Config
from tgbot.misc.scheduler import schedule_reminder_message
from tgbot.misc.sheet_amanger import GspreadManager


async def on_answer(m: Message, widget: Any, dialog_manager: DialogManager):
    ctx = dialog_manager.current_context()
    data = {'name': m.text, }
    await m.delete()
    ctx.dialog_data['data'] = data
    await dialog_manager.next(show_mode=ShowMode.EDIT)


async def on_calendar_input(c: CallbackQuery, widget: Button, dialog_manager: DialogManager):
    ctx = dialog_manager.current_context()

    logging.info(widget.widget_id)
    ctx.dialog_data['data']['date'] = widget.widget_id
    await dialog_manager.next(show_mode=ShowMode.EDIT)


async def calendar_input(m: Message, widget: Any, dialog_manager: DialogManager):
    ctx = dialog_manager.current_context()
    answer = m.text
    ctx.dialog_data['data']['date'] = answer
    await m.delete()
    await dialog_manager.next(show_mode=ShowMode.EDIT)


async def on_city(m: Message, widget: Any, dialog_manager: DialogManager):
    ctx = dialog_manager.current_context()
    answer = m.text
    ctx.dialog_data['data']['city'] = answer
    await m.delete()

    await dialog_manager.next(show_mode=ShowMode.EDIT)


async def skip_uni(c: CallbackQuery, widget: Any, dialog_manager: DialogManager):
    ctx = dialog_manager.current_context()
    ctx.dialog_data['data']['univercity'] = 'None'
    await dialog_manager.next(show_mode=ShowMode.EDIT)


async def on_univercity_input(m: Message, widget: Any, dialog_manager: DialogManager):
    ctx = dialog_manager.current_context()
    answer = m.text
    ctx.dialog_data['data']['univercity'] = answer
    await m.delete()
    await dialog_manager.next(show_mode=ShowMode.EDIT)


async def on_phone(m: Message, widget: Any, dialog_manager: DialogManager):
    ctx = dialog_manager.current_context()
    answer = m.text
    gspread_manager: GspreadManager = dialog_manager.middleware_data['sh_manager']
    scheduler: AsyncIOScheduler = dialog_manager.middleware_data['scheduler']

    user_id = dialog_manager.event.from_user.id
    date = ctx.start_data['date']
    ctx.dialog_data['data']['phone'] = answer


    await m.delete()
    data = ctx.dialog_data['data']
    data['event_date'] = date.strftime("%d.%m.%Y")
    data['city'] = ctx.start_data['city']
    data['user_id'] = user_id
    data['user_name'] = dialog_manager.event.from_user.username

    asyncio.create_task(
        gspread_manager.save_data(
            data,
        )
    )
    await schedule_reminder_message(scheduler, user_id, date, dialog_manager.event.bot)
    await m.bot.send_message(m.from_user.id,
                             'Вы успешно зарегистрированы на обучение, мы вам напомним о начале курсе в телеграме')
    await dialog_manager.done(show_mode=ShowMode.DELETE_AND_SEND)
