from typing import List

from passlib.context import CryptContext
from sqlalchemy.orm import class_mapper

# Create a CryptContext instance with bcrypt as the hashing scheme
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def clone_model(model):
    """
    Clone an SQLAlchemy model object without its primary key values.

    Args:
        model (object): The SQLAlchemy model instance to clone.

    Returns:
        dict: A dictionary containing the cloned model data without primary keys.

    Example:
        >>> clone_model(my_model)
        {"name": "example", "age": 30}

    Author:
        tranvanphuc.dev.it.2002@gmail.com
    """
    model.id
    table = model.__table__
    non_pk_columns = [k for k in table.columns.keys() if k not in table.primary_key]
    data = {c: getattr(model, c) for c in non_pk_columns}
    if "id" in data:
        data.pop("id")
    return data
