from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from model.ResultModel import ResultModel


async def create_result(
    db: AsyncSession,
    total_score: int,
    result_description_id: int,
    test_id: int,
    telegram_user_id: int
):
    db_result = ResultModel(
        total_score=total_score,
        result_description_id=result_description_id,
        test_id=test_id,
        telegram_user_id=telegram_user_id
    )
    db.add(db_result)
    await db.commit()
    return db_result
