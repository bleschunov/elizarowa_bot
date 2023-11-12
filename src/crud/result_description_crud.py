from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from model.ResultDescriptionModel import ResultDescriptionModel


async def read_relevant_result_description(db: AsyncSession, score: int):
    scalar_result = await db.scalars(
        select(ResultDescriptionModel)
        .where(ResultDescriptionModel.max_score < score)
        .order_by(ResultDescriptionModel.max_score.desc())
    )
    return scalar_result.first()


async def create_result_description(
    db: AsyncSession,
    text: str,
    max_score: int,
    test_id: int,
):
    db_result = ResultDescriptionModel(
        text=text,
        max_score=max_score,
        test_id=test_id
    )
    db.add(db_result)
    await db.commit()
    return db_result
