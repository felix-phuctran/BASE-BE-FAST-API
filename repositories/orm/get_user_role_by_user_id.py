import uuid
from typing import Optional

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from schema.dto.user_role_department_permission_dto import (
    UserRoleDepartmentPermissionDto,
)
from schema.response.user_response_schema import UserResponseSchema
from utils.logger import setup_logger

logger = setup_logger()

GET_USER_ROLE_ROLE_BY_USER_ID = f"""
    SELECT jsonb_build_object(
        'user', jsonb_build_object(
            '{UserResponseSchema.IS_ACTIVE}', u.is_active,
            '{UserResponseSchema.CREATED_AT}', u.created_at,
            '{UserResponseSchema.UPDATED_AT}', u.updated_at,
            '{UserResponseSchema.DELETED_AT}', u.deleted_at,
            '{UserResponseSchema.DISPLAY_NAME}', u.display_name,
            '{UserResponseSchema.EMAIL}', u.email,
            '{UserResponseSchema.PHONE_NUMBER}', u.phone_number,
            '{UserResponseSchema.AVATAR_URL}', u.avatar_url,
            '{UserResponseSchema.IS_VERIFIED}', u.is_verified,
            '{UserResponseSchema.VERIFICATION_CODE}', u.verification_code,
            '{UserResponseSchema.ID}', u.id
        ),
        
    )
    FROM users u
    JOIN roles r AND r.is_active = TRUE AND r.deleted_at IS NULL
    WHERE u.is_active = TRUE AND u.deleted_at IS NULL
    AND u.id = :user_id
    LIMIT 1;
"""


async def get_user_role_by_user_id(
    db: AsyncSession, user_id: uuid.UUID
) -> Optional[UserRoleDepartmentPermissionDto]:
    """
    Retrieve user details including role based on user_id.

    Args:
        db (AsyncSession): Asynchronous database session.
        user_id (UUID): User ID to fetch details for.

    Returns:
        Optional[UserRoleDepartmentPermissionDto]: The user-role details
        mapped to a DTO, or None if no data is found.
    """
    result = await db.execute(
        text(GET_USER_ROLE_ROLE_BY_USER_ID), {"user_id": str(user_id)}
    )
    row = result.fetchone()

    if row and row[0]:
        logger.info(f"UserRoleDepartmentPermissionDto: {row[0]}")
        return UserRoleDepartmentPermissionDto(**row[0])
    return None
