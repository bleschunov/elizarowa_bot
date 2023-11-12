def get_test_menu_inline_keyboard(test_id: int):
    buttons = [
        [
            InlineKeyboardButton(text="Pass the test", callback_data=f"pass_test_{test_id}"),
            InlineKeyboardButton(text="Edit the test", callback_data=f"edit_test_{test_id}")
        ],
        [InlineKeyboardButton(text="« Back to the all tests", callback_data=f"all_tests")]
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)