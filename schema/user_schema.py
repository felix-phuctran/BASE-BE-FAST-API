import uuid
from typing import ClassVar, Optional

from pydantic import BaseModel, EmailStr

from schema._soft_delete_schema import SoftDeleteSchema


class UserBaseSchema(BaseModel):
    DISPLAY_NAME: ClassVar[str] = "display_name"
    EMAIL: ClassVar[str] = "email"
    PHONE_NUMBER: ClassVar[str] = "phone_number"
    AVATAR_URL: ClassVar[str] = "avatar_url"
    IS_VERIFIED: ClassVar[str] = "is_verified"
    VERIFICATION_CODE: ClassVar[str] = "verification_code"

    display_name: str
    email: str
    phone_number: Optional[str]
    avatar_url: Optional[str]
    is_verified: bool
    verification_code: Optional[str]


class UserResponseSchema(UserBaseSchema, SoftDeleteSchema):
    ID: ClassVar[str] = "id"
    id: uuid.UUID

    class Config:
        from_attributes = True


class UserRoleDepartmentPermissionDto(BaseModel):
    user: UserResponseSchema


class UserCreateSchema(BaseModel):
    email: EmailStr
    password_hash: str
    display_name: str
    phone_number: str
    avatar_url: Optional[str] = None
    is_active: bool = True
    is_verified: bool = False
    verification_code: Optional[str] = None


class UserUpdateSchema(BaseModel):
    display_name: Optional[str]
    password_hash: Optional[str]
    email: Optional[str]
    phone_number: Optional[str]
    avatar_url: Optional[str]
    is_verified: Optional[bool]
    verification_code: Optional[str]
