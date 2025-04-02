import uuid
from datetime import datetime

from pydantic import BaseModel

from schema.base.user_session_base_schema import UserSessionBaseSchema


class UserSessionCreateSchema(BaseModel):
    user_id: uuid.UUID
    refresh_token: str
    expires_at: datetime  # Ensure this is a datetime object

    class Config:
        from_attributes = True
class UserSessionUpdateSchema(UserSessionBaseSchema):
    pass