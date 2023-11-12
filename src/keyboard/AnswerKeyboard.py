from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from model.AnswerModel import AnswerModel


def get_all_answers_inline_buttons(answers: list[AnswerModel]):
    buttons = []
    for a in answers:
        button = InlineKeyboardButton(text=a.text, callback_data=f"choose_answer_{a.id}")
        buttons.append([button])

    return InlineKeyboardMarkup(inline_keyboard=buttons)
