from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from model.TestModel import TestModel


def get_choose_test_inline_keyboard(test_models: list[TestModel]):
    buttons = []
    for test_model in test_models:
        buttons.append([InlineKeyboardButton(text=test_model.title, callback_data=f"choose_test_{test_model.id}")])

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_test_menu_inline_keyboard(test_id: int, is_admin: bool):
    first_row = [
        InlineKeyboardButton(text="Pass the test", callback_data=f"pass_test_{test_id}"),
    ]

    if is_admin:
        first_row.append(InlineKeyboardButton(text="Edit the test", callback_data=f"edit_test_{test_id}"))

    buttons = [
        first_row,
        [InlineKeyboardButton(text="« Back to the all tests", callback_data=f"all_tests")]
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_edit_test_inline_keyboard(test_id: int):
    buttons = [
        [
            InlineKeyboardButton(text="Edit title", callback_data=f"edit_title_test_{test_id}"),
            InlineKeyboardButton(text="Edit description", callback_data=f"edit_description_test_{test_id}")
        ],
        [
            InlineKeyboardButton(text="« Back to the test menu", callback_data=f"choose_test_{test_id}"),
            InlineKeyboardButton(text="« Back to the all tests", callback_data=f"all_tests")
        ]
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_test_back_inline_keyboard(test_id):
    buttons = [[
        InlineKeyboardButton(text="« Back to editing", callback_data=f"edit_test_{test_id}"),
        InlineKeyboardButton(text="« Back to the all tests", callback_data=f"all_tests")
    ]]

    return InlineKeyboardMarkup(inline_keyboard=buttons)
