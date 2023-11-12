from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from adapter.sheet import parse_tests
from crud.test_crud import create_test
from bot import dp, bot

new_test_router = Router()


class Form(StatesGroup):
    name = State()
    description = State()


@dp.message(F.content_type.in_({"document"}))
async def create_new_tests_by_file(message: Message, async_session: async_sessionmaker[AsyncSession]) -> None:
    filepath = "data/tests.xlsx"
    await bot.download(message.document, filepath)
    await parse_tests(async_session, filepath)
    await message.answer("Все тесты созданы")


@dp.message(Command("newtest"))
async def create_new_test(message: Message, state: FSMContext) -> None:
    await message.answer("Create new test. Please enter the test name:")
    await state.set_state(Form.name)


@new_test_router.message(Form.name)
async def process_name(message: Message, state: FSMContext) -> None:
    await state.update_data(title=message.text)
    await state.set_state(Form.description)
    await message.answer("Please enter the test description:")


@new_test_router.message(Form.description)
async def process_description(message: Message, state: FSMContext, async_session: async_sessionmaker[AsyncSession]) -> None:
    await state.update_data(description=message.text)
    data = await state.get_data()
    await state.clear()

    async with async_session.begin() as session:
        await create_test(session, data['title'], data['description'])

    await message.answer("New test created successfully!")
