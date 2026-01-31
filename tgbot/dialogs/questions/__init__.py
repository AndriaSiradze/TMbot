from aiogram_dialog import Dialog

from tgbot.dialogs.questions.window import name_window, birth_window, city_window, university_window, phone_window


def questions():
    return [
        Dialog(
            name_window(),
            birth_window(),
            city_window(),
            university_window(),
            phone_window(),
        )
    ]