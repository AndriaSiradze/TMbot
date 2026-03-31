import datetime
import operator

from aiogram.enums import ContentType
from aiogram_dialog import Window, DialogManager
from aiogram_dialog.widgets.kbd import Select, Column
from aiogram_dialog.widgets.media import StaticMedia
from aiogram_dialog.widgets.text import Format, Const
from aiohttp.web_fileresponse import content_type

from tgbot.dialogs.select_study.on_click import on_select_date, on_select_city
from tgbot.misc.states import SelectStudies
from tgbot.misc.studies import studies

base_text = """
Обучение Трансцендентальной Медитации:
5 очных занятий с учителем по 1.5 часа каждый день
27-31 марта Екатеринбург
11-15 апреля Челябинске
(точное время и место появится в нашем канале,
подписывайтесь и следите за новостями)

Стоимость обучения: 
2.000 руб при оплате до начала обучения
27 марта (Екатеринбург)
11 апреля (Челябинск)
3.000 руб — в день обучения
(стандартная цена обучения ТМ — 15.000 руб,
таким образом ваша скидка составит 80-87%)


Условия льготного обучения: 

Вам 18-25 лет
Вы подписаны на этот канал
Вам  все это интересно, и не терпится поскорее обучиться 🙂

Удачи вам, и мы очень надеемся всех вас увидеть на обучении, 
не упускайте этот поистине бесценный шанс, он может не повториться...

больше о Трансцендентальной Медитации тут:
www.pro-tm.ru
"""
def select_city():
    return Window(
        Format('{text}'),
        StaticMedia(
            path='tgbot/misc/img.png',
            media_params={'show_caption_above_media':True}
        ),
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
    cities = [k for k, v in studies.items()]
    text = base_text
    return {
        'cities': cities,
        'text': text
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
