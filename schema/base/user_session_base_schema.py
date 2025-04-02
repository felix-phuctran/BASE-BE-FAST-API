import uuid
from datetime import datetime
from typing import ClassVar

from pydantic import BaseModel


class UserSessionBaseSchema(BaseModel):
    USER_ID: ClassVar[str] = "user_id"
    REFRESH_TOKEN: ClassVar[str] = "refresh_token"
    EXPIRES_AT: ClassVar[str] = "expires_at"
    
    user_id: uuid.UUID
    refresh_token: str
    expires_at: datetime
    
    class Config:
        json_encoders = {
            datetime: lambda v: v  # Prevent automatic ISO string conversion
        }
