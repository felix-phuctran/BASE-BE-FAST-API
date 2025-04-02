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
    return unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()


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
    non_pk_columns = [k for k in table.columns.keys() if k not in table.primary_key]
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


import random
import re
import string

from slugify import slugify as slug_convert


def generate_random_string(length=128):
    """
    Generate a random string of a given length.

    Args:
        length (int): The length of the random string to generate. Defaults to 128.

    Returns:
        str: A randomly generated string of the specified length.

    Example:
        >>> generate_random_string(5)
        'aBcDe'

    Author:
        tranvanphuc.dev.it.2002@gmail.com
    """
    letters = list(string.ascii_letters + string.digits)
    random.shuffle(letters)
    random_string = "".join(random.choice(letters) for _ in range(length))
    return random_string


def generate_random_3(length=3):
    """
    Generate a random uppercase string of a given length.

    Args:
        length (int): The length of the random string to generate. Defaults to 3.

    Returns:
        str: A randomly generated uppercase string of the specified length.

    Example:
        >>> generate_random_3()
        'ABC'

    Author:
        tranvanphuc.dev.it.2002@gmail.com
    """
    letters = list(string.ascii_letters + string.digits)
    random.shuffle(letters)
    random_string = "".join(random.choice(letters) for _ in range(length))
    return random_string.upper()


def generate_account_id(length=22):
    """
    Generate a random account ID of a given length.

    Args:
        length (int): The length of the account ID to generate. Defaults to 22.

    Returns:
        str: A randomly generated account ID.

    Example:
        >>> generate_account_id()
        'A1B2C3D4E5F6G7H8I9J0KL'

    Author:
        tranvanphuc.dev.it.2002@gmail.com
    """
    letters = list(string.ascii_letters + string.digits)
    random.shuffle(letters)
    random_string = "".join(random.choice(letters) for _ in range(length))
    return random_string


def generate_chat_id(length=10):
    """
    Generate a random chat ID of a given length.

    Args:
        length (int): The length of the chat ID to generate. Defaults to 10.

    Returns:
        str: A randomly generated chat ID.

    Example:
        >>> generate_chat_id()
        '12345ABCDE'

    Author:
        tranvanphuc.dev.it.2002@gmail.com
    """
    letters = list(string.ascii_letters + string.digits)
    random.shuffle(letters)
    random_string = "".join(random.choice(letters) for _ in range(length))
    return random_string


def generate_number(length=6):
    """
    Generate a random numeric string of a given length.

    Args:
        length (int): The length of the numeric string to generate. Defaults to 6.

    Returns:
        str: A randomly generated numeric string.

    Example:
        >>> generate_number()
        '123456'

    Author:
        tranvanphuc.dev.it.2002@gmail.com
    """
    letters = string.digits
    return "".join(random.choice(letters) for _ in range(length))


def slugify(text):
    """
    Generate a slug from the input text, appending a random string for uniqueness.

    Args:
        text (str): The input text to slugify.

    Returns:
        str: A slugified string with a random suffix.

    Example:
        >>> slugify('Hello World')
        'hello-world-AbCd'

    Author:
        tranvanphuc.dev.it.2002@gmail.com
    """
    if not text:
        text = generate_account_id()
    text = slug_convert(text)
    random_string = "".join(random.choice(string.ascii_letters) for _ in range(4))
    slug = re.sub(r"[\W_]+", "-", text)
    return f"{slug}-{random_string}"


def slugify_title(text):
    """
    Generate a slug from the input text, prepending a random string for uniqueness.

    Args:
        text (str): The input text to slugify.

    Returns:
        str: A slugified string with a random prefix.

    Example:
        >>> slugify_title('Hello World')
        'AbC-hello-world'

    Author:
        tranvanphuc.dev.it.2002@gmail.com
    """
    text = slug_convert(text=text)
    random_string = "".join(random.choice(string.ascii_letters) for _ in range(3))
    slug = re.sub(r"[\W_]+", "-", text)
    return f"{random_string}-{slug}"


def generate_api_key(length=60):
    """
    Generate a random API key with a given length, prefixed with 'sk-'.

    Args:
        length (int): The length of the API key to generate (excluding the prefix). Defaults to 60.

    Returns:
        str: A randomly generated API key.

    Example:
        >>> generate_api_key()
        'sk-AbCdEfGhIjKlMnOpQrStUvWxYz1234567890'

    Author:
        tranvanphuc.dev.it.2002@gmail.com
    """
    letters = list(string.ascii_letters + string.digits)
    random.shuffle(letters)
    random_string = "".join(random.choice(letters) for _ in range(length))
    return "sk-" + random_string


from fastapi import Query

from utils.string_case import convert_filter_to_camel_case, to_snake_case


async def common_filter_parameters(
    page: int = 1,
    limit: int = 100,
    filter: str = "{}",
    include: str = None,
    join: str = "{}",
    orderBy: str = None,
):
    if join:
        join_ = convert_filter_to_camel_case(join)
    else:
        join_ = "{}"

    if filter:
        filter_ = convert_filter_to_camel_case(filter)
    else:
        filter_ = "{}"

    if include:
        include = to_snake_case(include)
    else:
        include = None
    skip = round((page - 1) * limit)
    if skip < 1:
        skip = 0
    if orderBy and orderBy != "":
        orderBy = to_snake_case(orderBy)
    else:
        orderBy = None
    return {
        "skip": skip,
        "limit": limit,
        "filter": filter_,
        "include": include,
        "order_by": orderBy,
        "join": join_,
    }


async def common_filter_parameters_and_actions(
    page: int = 1,
    limit: int = 100,
    filter: str = "{}",
    include: str = None,
    join: str = "{}",
    orderBy: str = None,
    action: str = "",
):
    if join:
        join_ = convert_filter_to_camel_case(join)
    else:
        join_ = "{}"

    if filter:
        filter_ = convert_filter_to_camel_case(filter)
    else:
        filter_ = "{}"

    if include:
        include = to_snake_case(include)
    else:
        include = None
    skip = round((page - 1) * limit)
    if skip < 1:
        skip = 0
    if orderBy and orderBy != "":
        orderBy = to_snake_case(orderBy)
    else:
        orderBy = None
    return {
        "skip": skip,
        "limit": limit,
        "filter": filter_,
        "include": include,
        "order_by": orderBy,
        "join": join_,
        "action": action,
    }


async def common_filter_parameters_with_id(
    page: int = 1,
    limit: int = 100,
    filter: str = "{}",
    include: str = None,
    join: str = "{}",
    orderBy: str = None,
    id: str = "",
):
    if join:
        join_ = convert_filter_to_camel_case(join)
    else:
        join_ = "{}"

    if filter:
        filter_ = convert_filter_to_camel_case(filter)
    else:
        filter_ = "{}"

    if include:
        include = to_snake_case(include)
    else:
        include = None
    skip = round((page - 1) * limit)
    if skip < 1:
        skip = 0
    if orderBy and orderBy != "":
        orderBy = to_snake_case(orderBy)
    else:
        orderBy = None
    return {
        "skip": skip,
        "limit": limit,
        "filter": filter_,
        "include": include,
        "order_by": orderBy,
        "join": join_,
        "id": id,
    }


async def search_pagination(page: int = 1, limit: int = 100, keyword: str = ""):
    return {"page": page, "limit": limit, "keyword": keyword}


async def actions(action: str = ""):
    return {"action": action}


async def actions_with_id(id: str = "", action: str = ""):
    return {"id": id, "action": action}


async def province_pagination(
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    code: str = "",
    name: str = "",
    created_at: str = "",
    updated_at: str = "",
):
    return {
        "limit": limit,
        "offset": offset,
        "code": code,
        "name": name,
        "created_at": created_at,
        "updated_at": updated_at,
    }


async def district_pagination(
    name: str = "",
    prefix: str = "",
    province_id: int = 0,
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    created_at: str = "",
    updated_at: str = "",
):
    return {
        "name": name,
        "prefix": prefix,
        "province_id": province_id,
        "limit": limit,
        "offset": offset,
        "created_at": created_at,
        "updated_at": updated_at,
    }


async def ward_pagination(
    name: str = "",
    prefix: str = "",
    tiki_ward_code: str = "",
    province_id: int = 297,
    district_id: int = 13,
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    created_at: str = "",
    updated_at: str = "",
):
    return {
        "name": name,
        "prefix": prefix,
        "tiki_ward_code": tiki_ward_code,
        "province_id": province_id,
        "district_id": district_id,
        "limit": limit,
        "offset": offset,
        "created_at": created_at,
        "updated_at": updated_at,
    }
