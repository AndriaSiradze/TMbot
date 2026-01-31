from aiogram_dialog import Dialog

from tgbot.dialogs.select_study.window import select_dates, select_city


def select_study_dlg():
    return [
        Dialog(
            select_city(),
            select_dates(),
        )
    ]