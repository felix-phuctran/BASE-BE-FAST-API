import uuid
from typing import ClassVar

from schema.base._soft_delete_schema import SoftDeleteSchema
from schema.base.user_base_schema import UserBaseSchema


class UserResponseSchema(UserBaseSchema, SoftDeleteSchema):
    ID: ClassVar[str] = "id"
    id: uuid.UUID
    
    class Config:
        from_attributes = True