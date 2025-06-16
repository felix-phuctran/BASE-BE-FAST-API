import logging
from datetime import datetime, timezone
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from constants.common import AppTranslationKeys
from repositories.base.orm_crud_base import ORMCRUDBase
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

    async def assign_role():
        """
        Assign a role to a user.

        This method is a placeholder for the actual implementation of assigning roles.
        It currently raises a NotImplementedError to indicate that this functionality
        needs to be implemented in the future.

        Raises:
            NotImplementedError: Indicates that the method is not yet implemented.
        """
        raise NotImplementedError("This method is not yet implemented.")
