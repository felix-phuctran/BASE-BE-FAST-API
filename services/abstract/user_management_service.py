from abc import ABC, abstractmethod
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from schema.request.user_management_request_schema import AssignRoleSchema


class UserManagementService(ABC):
    @abstractmethod
    async def assign_role(
        self,
        session_factory: async_sessionmaker[AsyncSession],
        assign_role_schema: AssignRoleSchema,
        admin_id: UUID,
    ):
        pass
