import os

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from bot import dp
from crud.test_crud import read_all_tests, read_test
from keyboard.TestKeyboard import get_choose_test_inline_keyboard, get_test_menu_inline_keyboard

edit_test_router = Router()


@dp.message(Command("all_tests"))
async def edit_test(message: Message, async_session: async_sessionmaker[AsyncSession]) -> None:
    async with async_session.begin() as session:
        tests = await read_all_tests(session)

    keyboard = get_choose_test_inline_keyboard(tests)
    await message.answer("Select a test:", reply_markup=keyboard)


@dp.callback_query(lambda c: c.data and c.data == "all_tests")
async def edit_test(callback_query: CallbackQuery, async_session: async_sessionmaker[AsyncSession]) -> None:
    async with async_session.begin() as session:
        tests = await read_all_tests(session)

    keyboard = get_choose_test_inline_keyboard(tests)
    await callback_query.message.edit_text("Select a test:", reply_markup=keyboard)


@dp.callback_query(lambda c: c.data and c.data.startswith('choose_test_'))
async def process_callback(
    callback_query: CallbackQuery,
    async_session: async_sessionmaker[AsyncSession]
) -> None:
    test_id = callback_query.data.split('_')[-1]

    async with async_session.begin() as session:
        test = await read_test(session, test_id)

    is_admin = callback_query.message.chat.id == int(os.getenv("ADMIN_TELEGRAM_ID"))
    keyboard = get_test_menu_inline_keyboard(int(test_id), is_admin)
    message = f"Title: {test.title}\nDescription: {test.description}"

    await callback_query.message.edit_text(message, reply_markup=keyboard)
