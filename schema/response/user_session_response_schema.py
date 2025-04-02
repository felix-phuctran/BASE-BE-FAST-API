import uuid
from typing import ClassVar

from schema.base._soft_delete_schema import SoftDeleteSchema
from schema.base.user_session_base_schema import UserSessionBaseSchema


class UserSessionResponseSchema(UserSessionBaseSchema, SoftDeleteSchema):
    ID: ClassVar[str] = "id"
    id: uuid.UUID
    
    class Config:
        from_attributes = True
