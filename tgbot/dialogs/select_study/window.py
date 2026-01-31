import datetime
import operator

from aiogram_dialog import Window, DialogManager
from aiogram_dialog.widgets.kbd import Select, Column
from aiogram_dialog.widgets.text import Format, Const

from tgbot.dialogs.select_study.on_click import on_select_date, on_select_city
from tgbot.misc.states import SelectStudies
from tgbot.misc.studies import studies


def select_city():
    return Window(
        Const('Запись на обучение:'),
        Column(
            Select(
                Format('{item}'),
                id='city_select',
                items='cities',
                item_id_getter=lambda x: x,
                on_click=on_select_city,
                type_factory=str
            ),
            id='city_items',
        ),
        state=SelectStudies.select_city,
        getter=cities_getter
    )


async def cities_getter(dialog_manager: DialogManager, **middleware_data):
    return {
        'cities': [k for k, v in studies.items()]
    }


def select_dates():
    return Window(
        Const('Выберите Дату'),
        Column(
            Select(
                Format('{item[spell]}'),
                id='dates_select',
                items='dates',
                item_id_getter=lambda item: item["datetime"].date().isoformat()                ,
                on_click=on_select_date,
                type_factory=datetime.datetime.fromisoformat
            ),
            id='dates_items'
        ),
        state=SelectStudies.select_date,
        getter=dates_getter
    )


async def dates_getter(dialog_manager: DialogManager, **middleware_data):
    ctx = dialog_manager.current_context()
    return {
        'dates': studies[ctx.dialog_data['city']]
    }
