from databases.users import Users

from repositories.base.orm_crud_base import ORMCRUDBase
from schema.user_schema import UserCreateSchema, UserUpdateSchema


class ORMCRUDUser(ORMCRUDBase[Users, UserCreateSchema, UserUpdateSchema]):
    pass


# Instance will be created in the container
