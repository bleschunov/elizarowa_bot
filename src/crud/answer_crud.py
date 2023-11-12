from sqlalchemy import delete, select, update

from model.AnswerModel import AnswerModel
from sqlalchemy.ext.asyncio import AsyncSession


async def create_answer(db: AsyncSession, text: str, description: str, score: int | str, question_id: int | str):
    db_answer = AnswerModel(text=text, description=description, score=int(score), question_id=int(question_id))
    db.add(db_answer)
    await db.commit()
    return db_answer


async def read_answers_by_ids(db: AsyncSession, answers_ids: list[str | int]):
    answers_ids = [int(i) for i in answers_ids]
    scalar_result = await db.scalars(select(AnswerModel).where(AnswerModel.id.in_(answers_ids)))
    return scalar_result.all()


async def read_all_answers_by_question_id(db: AsyncSession, question_id: int | str):
    scalar_result = await db.scalars(select(AnswerModel).filter_by(question_id=int(question_id)))
    return scalar_result.all()


async def update_answer(db: AsyncSession, answer_id: int | str, **patch):
    stmt = update(AnswerModel).where(AnswerModel.id == int(answer_id)).values(**patch)
    await db.execute(stmt)


async def delete_answer(db: AsyncSession, answer_id: int):
    stmt = delete(AnswerModel).where(AnswerModel.id == answer_id)
    await db.execute(stmt)
