from sqlalchemy import delete, select, update
from model.TestModel import TestModel
from sqlalchemy.ext.asyncio import AsyncSession


async def create_test(db: AsyncSession, title: str, description: str):
    db_test = TestModel(title=title, description=description)
    db.add(db_test)
    await db.commit()
    return db_test


async def read_test(db: AsyncSession, test_id: int | str):
    scalar_result = await db.scalars(select(TestModel).filter_by(id=int(test_id)))
    return scalar_result.first()


async def read_all_tests(db: AsyncSession):
    scalar_result = await db.scalars(select(TestModel))
    return scalar_result.all()


async def update_test(db: AsyncSession, test_id: int | str, **patch):
    stmt = update(TestModel).where(TestModel.id == int(test_id)).values(**patch)
    await db.execute(stmt)


async def delete_test(db: AsyncSession, test_id: int):
    stmt = delete(TestModel).where(TestModel.id == test_id)
    await db.execute(stmt)
