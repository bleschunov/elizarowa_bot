from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from bot import dp
from crud import question_crud, answer_crud, result_description_crud, result_crud
from keyboard.AnswerKeyboard import get_all_answers_inline_buttons


async def get_total_score(async_session: async_sessionmaker[AsyncSession], answers_ids: list[int]) -> int:
    async with async_session() as session:
        answers = await answer_crud.read_answers(session, answers_ids)
    return sum(a.score for a in answers)


@dp.callback_query(lambda c: c.data and c.data.startswith('pass_test_'))
async def start_test(
    callback_query: CallbackQuery,
    async_session: async_sessionmaker[AsyncSession],
    state: FSMContext
) -> None:
    test_id = callback_query.data.split('_')[-1]

    async with async_session() as session:
        questions = await question_crud.read_all_questions_by_test_id(session, test_id)
        first_question = questions[0]
        first_question_answers = await answer_crud.read_all_answers_by_question_id(session, first_question.id)

    keyboard = get_all_answers_inline_buttons(first_question_answers)
    message = f"{first_question.text}"

    await state.update_data(test_id=test_id, questions=questions, last_question_index=0, answers_ids=[])
    await callback_query.message.edit_text(message, reply_markup=keyboard)


@dp.callback_query(lambda c: c.data and c.data.startswith('choose_answer_'))
async def answer_question(
        callback_query: CallbackQuery,
        async_session: async_sessionmaker[AsyncSession],
        state: FSMContext
) -> None:
    new_answer_id = callback_query.data.split('_')[-1]

    prev_data = await state.get_data()
    next_question_index = prev_data["last_question_index"] + 1
    prev_answers_ids = prev_data["answers_ids"]

    questions = prev_data["questions"]
    if len(questions) == next_question_index:
        answers_ids = [*prev_answers_ids, new_answer_id]
        async with async_session() as session:
            answers = await answer_crud.read_answers_by_ids(session, answers_ids)
            total_score = sum(a.score for a in answers)
            result_description = await result_description_crud.read_relevant_result_description(
                session, score=total_score
            )
            await result_crud.create_result(
                session,
                total_score=total_score,
                result_description_id=result_description.id,
                test_id=prev_data["test_id"],
                telegram_user_id=callback_query.message.from_user.id
            )
        await callback_query.message.answer(f"Вы прошли тест! Ваш результат:\n{result_description.text}")
        return

    next_question = prev_data["questions"][next_question_index]

    async with async_session() as session:
        next_question_answers = await answer_crud.read_all_answers_by_question_id(session, next_question.id)

    keyboard = get_all_answers_inline_buttons(next_question_answers)
    message = f"{next_question.text}"

    await state.update_data(last_question_index=next_question_index, answer_ids=[*prev_answers_ids, new_answer_id])
    await callback_query.message.edit_text(message, reply_markup=keyboard)
