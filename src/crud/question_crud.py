from sqlalchemy import delete, select, update

from model.QuestionModel import QuestionModel
from sqlalchemy.ext.asyncio import AsyncSession


async def create_question(db: AsyncSession, text: str, test_id: int | str):
    db_question = QuestionModel(text=text, test_id=int(test_id))
    db.add(db_question)
    await db.commit()
    return db_question


async def read_question(db: AsyncSession, question_id: int | str):
    scalar_result = await db.scalars(select(QuestionModel).filter_by(id=int(question_id)))
    return scalar_result.first()


async def read_all_questions_by_test_id(db: AsyncSession, test_id: int | str):
    scalar_result = await db.scalars(select(QuestionModel).filter_by(test_id=int(test_id)))
    return scalar_result.all()


async def update_question(db: AsyncSession, question_id: int | str, **patch):
    stmt = update(QuestionModel).where(QuestionModel.id == int(question_id)).values(**patch)
    await db.execute(stmt)


async def delete_question(db: AsyncSession, question_id: int):
    stmt = delete(QuestionModel).where(QuestionModel.id == question_id)
    await db.execute(stmt)
