import uuid
from typing import Optional

from pydantic import BaseModel, EmailStr, Field

from schema.base.user_base_schema import UserBaseSchema


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
