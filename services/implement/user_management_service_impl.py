import logging
from datetime import datetime, timezone
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from constants.common import AppTranslationKeys
from repositories.base.orm_crud_base import ORMCRUDBase
from schema.request.user_management_request_schema import AssignRoleSchema
from services.abstract.user_management_service import UserManagementService
from utils.logger import handle_response


class UserManagementServiceImpl(UserManagementService):
    def __init__(
        self,
        logger: logging.Logger,
        translation: AppTranslationKeys,
        orm_crud_user: ORMCRUDBase,
    ):
        self._logger = logger
        self._translation = translation
        self._orm_crud_user = orm_crud_user

    async def assign_role(
        self,
        session_factory: async_sessionmaker[AsyncSession],
        assign_role_schema: AssignRoleSchema,
        admin_id: UUID,
    ):
        """
        Assign a role to a user

        Args:
            session_factory: Database session factory
            assign_role_schema: Role assignment request data
            admin_id: ID of the admin performing the action

        Returns:
            Dict: Response with success message

        Raises:
            HTTPException: If user or role not found, or operation fails
        """
        self._logger.info(
            f"Assigning role {assign_role_schema.role_id} to user {assign_role_schema.user_id} by admin {admin_id}"
        )

        try:
            async with session_factory() as db:
                # Check if user exists
                user = await self._orm_crud_user.get_one_by(
                    db=db, filter={"id": assign_role_schema.user_id}
                )

                if not user:
                    self._logger.error(f"User not found: {assign_role_schema.user_id}")
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=self._translation.User["NotFound"],
                    )

                # Check if role exists
                role = await self._orm_crud_role.get_one_by(
                    db=db, filter={"id": assign_role_schema.role_id}
                )

                if not role:
                    self._logger.error(f"Role not found: {assign_role_schema.role_id}")
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=self._translation.Role["RoleNotFound"],
                    )

                # Get previous role for audit
                previous_role_id = user.role_id

                # Update user's role
                user_update = await self._orm_crud_user.update(
                    db=db,
                    db_obj=user,
                    obj_in={
                        "role_id": assign_role_schema.role_id,
                        "updated_at": datetime.now(timezone.utc),
                    },
                )

                if not user_update:
                    self._logger.error(f"Failed to update role for user {user.id}")
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail=self._translation.User["UserUpdateFailed"],
                    )

                # Create audit entry
                # audit_data = Audits(
                #     user_id=admin_id,
                #     org_id=user.org_id,
                #     action="role_changed",
                #     table_name="users",
                #     record_id=user.id,
                #     details=f"Role changed from {previous_role_id} to {assign_role_schema.role_id}",
                # )

                # await self._orm_crud_audit.save(db, audit_data)

                return handle_response(
                    message=self._translation.User["RoleAssignSuccess"],
                    status_code=status.HTTP_200_OK,
                )

        except HTTPException:
            raise
        except Exception as e:
            self._logger.error(f"Error in assign_role: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=self._translation.User["RoleAssignFailed"],
            )
