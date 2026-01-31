import asyncio
import logging
from typing import Any

from aiogram.types import Message, CallbackQuery
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.kbd import Button

from tgbot.config import Config


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


async def save_data(data: dict, config: Config):
    agcm = await config.gspread_conf.agcm.authorize()
    sheet = await agcm.open('TMsheet')
    wk = await sheet.get_worksheet(0)
    logging.info(data)
    await wk.append_row(
        [
            data['city'],
            data['event_date'],
            data['name'],
            data['univercity'],
            data['phone'],
            data['date'],
            data['user_name'],
            data['user_id']]
    )


async def on_phone(m: Message, widget: Any, dialog_manager: DialogManager):
    ctx = dialog_manager.current_context()
    answer = m.text
    config: Config = dialog_manager.middleware_data['config']
    ctx.dialog_data['data']['phone'] = answer
    await m.delete()
    data = ctx.dialog_data['data']
    data['event_date'] = ctx.start_data['date'].strftime("%d.%m.%Y")
    data['city'] = ctx.start_data['city']
    data['user_id'] = dialog_manager.event.from_user.id
    data['user_name'] = dialog_manager.event.from_user.username
    asyncio.create_task(
        save_data(
            data,
            config
        )
    )
    await m.bot.send_message(m.from_user.id, 'Ваша анкета сохранена мы с вами свяжемся по указанному номеру ')
    await dialog_manager.done(show_mode=ShowMode.DELETE_AND_SEND)
