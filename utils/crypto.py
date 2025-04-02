import re
import unicodedata
from typing import List

from passlib.context import CryptContext
from sqlalchemy.orm import class_mapper

# Create a CryptContext instance with bcrypt as the hashing scheme
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(password: str) -> str:
    """
    Hash a password using the bcrypt scheme.

    Args:
        password (str): The password to be hashed.

    Returns:
        str: The hashed password.

    Example:
        >>> hash("my_password")
        "$2b$12$..."

    Author:
        tranvanphuc.dev.it.2002@gmail.com
    """
    return pwd_context.hash(password)

def verify(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against a hashed password.

    Args:
        plain_password (str): The plain text password to be verified.
        hashed_password (str): The hashed password to verify against.

    Returns:
        bool: True if the password matches the hashed password, False otherwise.

    Example:
        >>> verify("my_password", "$2b$12$...")
        True

    Author:
        tranvanphuc.dev.it.2002@gmail.com
    """
    return pwd_context.verify(plain_password, hashed_password)

def ascii(text: str) -> str:
    """
    Convert a string to ASCII characters only, while preserving 'Đ' and 'đ'.

    Args:
        text (str): The input string to be converted.

    Returns:
        str: The ASCII-converted string.

    Example:
        >>> ascii("Đây là ví dụ")
        "Day la vi du"

    Author:
        tranvanphuc.dev.it.2002@gmail.com
    """
    text = text.replace("Đ", "D").replace("đ", "d")
    return (
        unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    )

def slugify(value: str) -> str:
    """
    Convert a string to a slug that is URL-friendly, while preserving 'Đ' and 'đ'.

    Args:
        value (str): The input string to be converted to a slug.

    Returns:
        str: The slugified string.

    Example:
        >>> slugify("Đây là ví dụ")
        "day-la-vi-du"

    Author:
        tranvanphuc.dev.it.2002@gmail.com
    """
    value = value.replace("Đ", "D").replace("đ", "d")
    value = unicodedata.normalize("NFKD", value)
    value = value.encode("ascii", "ignore").decode("ascii")
    value = re.sub(r"\s+", "-", value.lower())
    value = re.sub(r"[^a-z0-9-]", "", value)
    value = re.sub(r"-+", "-", value)
    value = value.strip("-")
    return value

def pick_(source: any, keys: List[str]) -> dict:
    """
    Extract specific keys from a source object or dictionary.

    Args:
        source (any): The source object or dictionary.
        keys (List[str]): A list of keys to extract from the source.

    Returns:
        dict: A dictionary containing the extracted key-value pairs.

    Example:
        >>> pick_({"a": 1, "b": 2}, ["a"])
        {"a": 1}

    Author:
        tranvanphuc.dev.it.2002@gmail.com
    """
    if type(source) is dict:
        return {key: source[key] for key in keys}
    return {key: getattr(source, key) for key in keys}

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
    non_pk_columns = [
        k for k in table.columns.keys() if k not in table.primary_key
    ]
    data = {c: getattr(model, c) for c in non_pk_columns}
    if "id" in data:
        data.pop("id")
    return data

def asdict(obj):
    """
    Convert a SQLAlchemy object to a dictionary.

    Args:
        obj (object): The SQLAlchemy object to convert.

    Returns:
        dict: A dictionary representation of the SQLAlchemy object.

    Example:
        >>> asdict(my_model)
        {"id": 1, "name": "example"}

    Author:
        tranvanphuc.dev.it.2002@gmail.com
    """
    return dict(
        (col.name, getattr(obj, col.name))
        for col in class_mapper(obj.__class__).mapped_table.c
    )
