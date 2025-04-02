from models.user_sessions import UserSessions
from repositories.base.orm_crud_base import ORMCRUDBase
from schema.request.user_session_request_schema import (
    UserSessionCreateSchema,
    UserSessionUpdateSchema,
)


class ORMCRUDUserSession(
    ORMCRUDBase[UserSessions, UserSessionCreateSchema, UserSessionUpdateSchema]
):
    pass


# Instance will be created in the container
