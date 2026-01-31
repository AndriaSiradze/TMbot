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
    skip_uni, calendar_input, on_calendar_input
from tgbot.misc.states import QuestionAnswer


def _locale(manager: DialogManager) -> str:
    # Always Russian:
    return "ru"  # or "ru_RU"
    # Or user-based:
    # lc = (manager.event.from_user.language_code or "ru").replace("-", "_")
    # return lc


class WeekDay(Text):
    async def _render_text(self, data, manager: DialogManager) -> str:
        d: date = data["date"]
        return get_day_names(width="short", context="stand-alone", locale=_locale(manager))[d.weekday()].title()


class Month(Text):
    async def _render_text(self, data, manager: DialogManager) -> str:
        d: date = data["date"]
        return get_month_names("wide", context="stand-alone", locale=_locale(manager))[d.month].title()


class RuCalendar(Calendar):
    def _init_views(self) -> dict[CalendarScope, CalendarScopeView]:
        return {
            CalendarScope.DAYS: CalendarDaysView(
                self._item_callback_data,
                date_text=DATE_TEXT,
                today_text=TODAY_TEXT,
                header_text=Month() + " " + Format("{date:%Y}"),
                weekday_text=WeekDay(),
                next_month_text=Month() + " >>",
                prev_month_text="<< " + Month(),
            ),
            CalendarScope.MONTHS: CalendarMonthView(
                self._item_callback_data,
                month_text=Month(),
                header_text=Format("{date:%Y}"),
            ),
            CalendarScope.YEARS: CalendarYearsView(self._item_callback_data),
        }


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
        MessageInput(func=calendar_input),
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
