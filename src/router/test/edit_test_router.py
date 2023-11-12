from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from bot import dp
from crud.test_crud import read_all_tests, update_test, read_test
from keyboard.TestKeyboard import get_edit_test_inline_keyboard, get_test_back_inline_keyboard

edit_test_router = Router()


class EditTestTitle(StatesGroup):
    title = State()


@dp.callback_query(lambda c: c.data and c.data.startswith('edit_test_'))
async def process_callback(callback_query: CallbackQuery, async_session: async_sessionmaker[AsyncSession]) -> None:
    test_id = callback_query.data.split('_')[-1]

    async with async_session() as session:
        test = await read_test(session, test_id)

    keyboard = get_edit_test_inline_keyboard(int(test_id))
    message = f"Title: {test.title}\nDescription: {test.description}\n\nWhat do you want to edit?"

    await callback_query.message.edit_text(message, reply_markup=keyboard)


@dp.callback_query(lambda c: c.data and c.data.startswith('edit_title_test_'))
async def process_callback(callback_query: CallbackQuery, state: FSMContext) -> None:
    test_id = callback_query.data.split('_')[-1]
    await state.update_data(test_id=test_id)
    await state.set_state(EditTestTitle.title)
    await callback_query.message.answer("Input new test title")


@edit_test_router.message(EditTestTitle.title)
async def process_id(message: Message, state: FSMContext, async_session: async_sessionmaker[AsyncSession]) -> None:
    await state.update_data(new_test_title=message.text)
    data = await state.get_data()
    await state.clear()

    async with async_session.begin() as session:
        await update_test(session, data["test_id"], title=data["new_test_title"])

    keyboard = get_test_back_inline_keyboard(data["test_id"])
    await message.answer("Test is updated", reply_markup=keyboard)


# @dp.message(Command("edittest"))
# async def edit_test(message: Message, async_session: async_sessionmaker[AsyncSession]) -> None:
#     async with async_session() as session:
#         tests = await read_all_tests(session)
#
#     buttons = []
#     for test in tests:
#         buttons.append([InlineKeyboardButton(text=test.title, callback_data=f"edit_{test.id}")])
#     keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
#     await message.answer("Select a test to edit:", reply_markup=keyboard)
#
#
# @dp.callback_query(lambda c: c.data and c.data.startswith('edit_'))
# async def process_callback(callback_query: CallbackQuery, state: FSMContext) -> None:
#     _, test_id = callback_query.data.split('_')
#     await state.update_data(id=int(test_id))
#     await state.set_state(EditForm.name)
#     await callback_query.message.answer("Please enter the new test name:")
#
#
# @edit_test_router.message(EditForm.id)
# async def process_id(message: Message, state: FSMContext) -> None:
#     await state.update_data(id=int(message.text))
#     await state.set_state(EditForm.name)
#     await message.answer("Please enter the new test name:")
#
#
# @edit_test_router.message(EditForm.name)
# async def process_name(message: Message, state: FSMContext) -> None:
#     await state.update_data(name=message.text)
#     await state.set_state(EditForm.description)
#     await message.answer("Please enter the new test description:")
#
#
# @edit_test_router.message(EditForm.description)
# async def process_description(message: Message, state: FSMContext, async_session: async_sessionmaker[AsyncSession]) -> None:
#     await state.update_data(description=message.text)
#     data = await state.get_data()
#     await state.clear()
#
#     async with async_session() as session:
#         await update_test(session, data['id'], data['name'], data['description'])
#
#     await message.answer("Test updated successfully!")
#
