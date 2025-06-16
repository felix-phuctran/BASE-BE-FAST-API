from abc import ABC, abstractmethod
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker


class UserManagementService(ABC):
    @abstractmethod
    async def assign_role(
        self,
        session_factory: async_sessionmaker[AsyncSession],
        admin_id: UUID,
    ):
        pass
