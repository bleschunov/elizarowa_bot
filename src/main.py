import asyncio
import logging
import sys

from aiogram.filters import Command
from aiogram.types import Message
from dotenv import load_dotenv

from db import async_session
from router.test import get_test_router
from router.test import pass_test_router
from router.test.new_test_router import new_test_router
from router.test.edit_test_router import edit_test_router
from bot import bot, dp

load_dotenv()


@dp.message(Command("start"))
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Hello, {message.from_user.full_name}!")


async def main() -> None:
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    dp.include_router(new_test_router)
    dp.include_router(edit_test_router)
    await dp.start_polling(bot, async_session=async_session)


if __name__ == "__main__":
    asyncio.run(main())
