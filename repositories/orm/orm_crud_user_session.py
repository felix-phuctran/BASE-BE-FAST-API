from databases.user_sessions import UserSessions

from repositories.base.orm_crud_base import ORMCRUDBase
from schema.user_session_schema import UserSessionCreateSchema, UserSessionUpdateSchema


class ORMCRUDUserSession(
    ORMCRUDBase[UserSessions, UserSessionCreateSchema, UserSessionUpdateSchema]
):
    pass


# Instance will be created in the container
