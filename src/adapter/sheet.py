import openpyxl
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from crud import test_crud, result_description_crud
from crud import question_crud
from crud import answer_crud


async def parse_tests(async_session: async_sessionmaker[AsyncSession], filepath: str):
    wb = openpyxl.load_workbook(filepath)
    ws = wb.active

    first = True
    current_test_id = None
    current_question_id = None

    for row in ws.rows:
        if first:
            first = False
            continue

        if row[0].value is not None:
            async with async_session.begin() as session:
                test = await test_crud.create_test(
                    session,
                    title=row[0].value,
                    description=row[1].value
                )
                current_test_id = test.id
                continue

        if row[2].value is not None:
            async with async_session.begin() as session:
                question = await question_crud.create_question(
                    session,
                    text=row[2].value,
                    test_id=current_test_id
                )
                current_question_id = question.id
                continue

        if row[3].value is not None:
            async with async_session.begin() as session:
                await answer_crud.create_answer(
                    session,
                    text=row[3].value,
                    description=row[4].value,
                    score=row[5].value,
                    question_id=current_question_id
                )

        if row[6].value is not None:
            async with async_session.begin() as session:
                await result_description_crud.create_result_description(
                    session,
                    text=row[7].value,
                    max_score=row[6].value,
                    test_id=current_test_id
                )
