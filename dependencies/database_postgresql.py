from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from dependencies.session import AsyncSessionLocal


def get_orgs_db_factory() -> async_sessionmaker[AsyncSession]:
    return AsyncSessionLocal
