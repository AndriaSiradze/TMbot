from tgbot.dialogs.questions import questions
from tgbot.dialogs.select_study import select_study_dlg

dialog_router_list = [
    *select_study_dlg(),
    *questions()
]
