from datetime import date

from aiogram_dialog import DialogManager
from aiogram_dialog import Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Calendar, CalendarScope, Button, Group
from aiogram_dialog.widgets.kbd.calendar_kbd import (
    CalendarDaysView, CalendarMonthView, CalendarYearsView, CalendarScopeView,
    DATE_TEXT, TODAY_TEXT,
)
from aiogram_dialog.widgets.text import Const
from aiogram_dialog.widgets.text import Text, Format
from babel.dates import get_day_names, get_month_names

from tgbot.dialogs.questions.on_click import on_answer, on_phone, on_univercity_input, on_city, \
    skip_uni, on_calendar_input
from tgbot.misc.states import QuestionAnswer


def name_window():
    return Window(
        Const("Фамилия, Имя Отчество"),
        MessageInput(func=on_answer),
        state=QuestionAnswer.name,
    )


def birth_window():
    return Window(
        Const("Сколько вам лет ?"),
        Group(
        *[
            Button(Const(str(i)), id=str(i), on_click=on_calendar_input) for i in range(18, 36)
        ],
        Button(Const('35+'), id='35plus', on_click=on_calendar_input),
            id='age_group',
            width=3
        ),
        # MessageInput(func=calendar_input),
        state=QuestionAnswer.age,
    )


def city_window():
    return Window(
        Const("Введите Город"),
        MessageInput(func=on_city),
        state=QuestionAnswer.city,
    )


def university_window():
    return Window(
        Const("ВУЗ"),
        MessageInput(func=on_univercity_input),
        Button(Const('Пропустить'), id='skip', on_click=skip_uni),
        state=QuestionAnswer.university,
    )


def phone_window():
    return Window(
        Const("Контактный телефон"),
        MessageInput(func=on_phone),
        state=QuestionAnswer.phone,
    )
