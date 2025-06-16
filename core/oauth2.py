from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Union
from uuid import UUID

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from constants.common import AppTranslationKeys
from core.env import env
from dependencies import database_postgresql
from repositories.orm.get_user_role_by_user_id import get_user_role_by_user_id
from schema.user_schema import UserRoleDepartmentPermissionDto

# Initialize translation
translation = AppTranslationKeys()

# OAuth2 configuration
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/sign-in")

# Common exceptions with translated messages
CREDENTIALS_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail=translation.Auth["InvalidCredentials"],
    headers={"WWW-Authenticate": "Bearer"},
)

PERMISSION_EXCEPTION = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail=translation.Auth["NotEnoughPermissions"],
)

TOKEN_EXPIRED_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail=translation.Auth["TokenExpired"],
    headers={"WWW-Authenticate": "Bearer"},
)

INVALID_TOKEN_TYPE_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail=translation.Auth["InvalidTokenType"],
    headers={"WWW-Authenticate": "Bearer"},
)

USER_NOT_FOUND_EXCEPTION = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail=translation.Auth["UserNotFound"],
)

INACTIVE_USER_EXCEPTION = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail=translation.Auth["InactiveUser"],
)

UNVERIFIED_USER_EXCEPTION = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail=translation.Auth["UnverifiedUser"],
)

ADMIN_REQUIRED_EXCEPTION = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail=translation.Auth["AdminRequired"],
)


class TokenData:
    """Token data structure for JWT payload"""

    def __init__(
        self,
        user_id: UUID,
        mode: str = "access_token",
        exp: Optional[datetime] = None,
        iat: Optional[datetime] = None,
        **kwargs
    ):
        self.user_id = user_id
        self.mode = mode
        self.exp = exp
        self.iat = iat or datetime.utcnow()
        for key, value in kwargs.items():
            setattr(self, key, value)

    def to_dict(self) -> Dict[str, Any]:
        """Convert token data to dictionary for JWT encoding"""
        result = {
            "user_id": str(self.user_id),
            "mode": self.mode,
            "iat": int(self.iat.timestamp()),
        }

        if self.exp:
            result["exp"] = int(self.exp.timestamp())

        # Add any additional attributes
        for key, value in self.__dict__.items():
            if key not in ["user_id", "mode", "exp", "iat"]:
                result[key] = value

        return result


def create_access_token(user_id: Union[str, UUID], **additional_data) -> str:
    """
    Create a new JWT access token

    Args:
        user_id: User identifier
        additional_data: Additional data to include in the token

    Returns:
        str: Encoded JWT access token
    """
    expiration = datetime.utcnow() + timedelta(days=env.JWT_ACCESS_TOKEN_EXP_DAYS)

    token_data = TokenData(
        user_id=UUID(str(user_id)) if isinstance(user_id, str) else user_id,
        mode="access_token",
        exp=expiration,
        **additional_data
    )

    return jwt.encode(
        token_data.to_dict(), env.JWT_SECRET_KEY, algorithm=env.JWT_ALGORITHM
    )


def create_refresh_token(user_id: Union[str, UUID], **additional_data) -> str:
    """
    Create a new JWT refresh token

    Args:
        user_id: User identifier
        additional_data: Additional data to include in the token

    Returns:
        str: Encoded JWT refresh token
    """
    expiration = datetime.utcnow() + timedelta(days=env.JWT_REFRESH_TOKEN_EXP_DAYS)

    token_data = TokenData(
        user_id=UUID(str(user_id)) if isinstance(user_id, str) else user_id,
        mode="refresh_token",
        exp=expiration,
        **additional_data
    )

    return jwt.encode(
        token_data.to_dict(), env.JWT_SECRET_KEY, algorithm=env.JWT_ALGORITHM
    )


async def decode_token(token: str) -> Dict[str, Any]:
    """
    Decode and validate JWT token

    Args:
        token: JWT token string

    Returns:
        Dict: Decoded token payload

    Raises:
        HTTPException: If token is invalid or expired
    """
    try:
        payload = jwt.decode(token, env.JWT_SECRET_KEY, algorithms=[env.JWT_ALGORITHM])

        # Check if token has required fields
        if "user_id" not in payload or "mode" not in payload:
            raise CREDENTIALS_EXCEPTION

        # Check if token has expired
        if "exp" in payload and datetime.utcnow().timestamp() > payload["exp"]:
            raise TOKEN_EXPIRED_EXCEPTION

        return payload
    except JWTError:
        raise CREDENTIALS_EXCEPTION


async def get_current_user_data(
    token: str = Depends(oauth2_scheme),
    session_factory: async_sessionmaker[AsyncSession] = Depends(
        database_postgresql.get_orgs_db_factory
    ),
) -> UserRoleDepartmentPermissionDto:
    """
    Get current authenticated user with role

    Args:
        token: JWT token from request
        session_factory: Async session factory for database access

    Returns:
        UserRoleDepartmentPermissionDto: User data with role

    Raises:
        HTTPException: If user is not authenticated or not found
    """
    payload = await decode_token(token)

    # Verify token is an access token
    if payload["mode"] != "access_token":
        raise INVALID_TOKEN_TYPE_EXCEPTION

    user_id = UUID(payload["user_id"])

    # Get user with role using async session
    async with session_factory() as db:
        user_data = await get_user_role_by_user_id(db, user_id)

        if not user_data:
            raise USER_NOT_FOUND_EXCEPTION

        return user_data


class RBACDependency:
    """
    Role-Based Access Control dependency for FastAPI endpoints

    This class creates a callable dependency that can be used to protect
    API endpoints based on user roles.
    """

    def __init__(
        self, required_roles: Optional[List[str]] = None, verify_org: bool = True
    ):
        """
        Initialize RBAC dependency

        Args:
            required_roles: List of role names required to access the endpoint
            verify_org: Whether to verify organization in the service layer
        """
        self.required_roles = required_roles or []
        self.verify_org = verify_org

    async def __call__(
        self,
        request: Request,
        user_data: UserRoleDepartmentPermissionDto = Depends(get_current_user_data),
    ) -> UserRoleDepartmentPermissionDto:
        """
        Verify user has required roles

        Args:
            request: FastAPI request object
            user_data: User data with role

        Returns:
            UserRoleDepartmentPermissionDto: User data if authorized

        Raises:
            HTTPException: If user doesn't have required roles
        """
        # Check if user is active
        if not user_data.user.is_active:
            raise INACTIVE_USER_EXCEPTION

        # Check if user is verified
        if not user_data.user.is_verified:
            raise UNVERIFIED_USER_EXCEPTION

        # Check role-based access
        if self.required_roles and user_data.role.name not in self.required_roles:
            raise PERMISSION_EXCEPTION

        # Store organization ID in request state for service layer verification
        if self.verify_org and user_data.user.org_id:
            request.state.org_id = user_data.user.org_id

        return user_data


# Predefined RBAC dependencies for common use cases
require_admin = RBACDependency(required_roles=["admin"])
require_manager = RBACDependency(required_roles=["admin", "manager"])
require_user = RBACDependency()  # Just requires authentication


async def require_admin(
    user_data: UserRoleDepartmentPermissionDto = Depends(get_current_user_data),
) -> UserRoleDepartmentPermissionDto:
    """
    Dependency to require admin role for endpoints

    Args:
        user_data: User data including role information

    Returns:
        UserRoleDepartmentPermissionDto: The user data if the user has admin role

    Raises:
        HTTPException: If user doesn't have admin role
    """
    # Check if user has admin role (modify this based on your role system)
    if user_data.role.name.lower() != "admin":
        raise ADMIN_REQUIRED_EXCEPTION
    return user_data
