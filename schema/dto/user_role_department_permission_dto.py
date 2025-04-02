from pydantic import BaseModel

from schema.response.user_response_schema import UserResponseSchema


class UserRoleDepartmentPermissionDto(BaseModel):
    user: UserResponseSchema
