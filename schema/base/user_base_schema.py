import uuid
from typing import ClassVar, Optional

from pydantic import BaseModel


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
