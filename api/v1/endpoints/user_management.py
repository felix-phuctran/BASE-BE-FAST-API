# WARN: Code is written but not yet tested

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from container.container import container
from core.oauth2 import require_user
from dependencies import database_postgresql
from schema.dto.user_role_department_permission_dto import (
    UserRoleDepartmentPermissionDto,
)
from schema.request.user_management_request_schema import (
    AssignRoleSchema,
    LockUnlockAccountSchema,
)
from services.abstract.user_management_service import UserManagementService

router = APIRouter()
user_management_service: UserManagementService = container.get_user_management_service()


@router.post(
    "/users/assign-role",
    status_code=status.HTTP_200_OK,
)
async def assign_role(
    assign_role_schema: AssignRoleSchema,
    user: UserRoleDepartmentPermissionDto = Depends(require_user),
    session_factory: async_sessionmaker[AsyncSession] = Depends(
        database_postgresql.get_orgs_db_factory
    ),
):
    """
    Assign a role to a user

    This endpoint allows administrators to assign roles to users.
    Requires admin privileges.

    Payload:
    {
        "user_id": "uuid",
        "role_id": "uuid"
    }
    """
    return await user_management_service.assign_role(
        session_factory=session_factory,
        assign_role_schema=assign_role_schema,
        user=user,
    )
