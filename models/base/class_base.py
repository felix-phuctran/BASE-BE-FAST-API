import uuid
from datetime import datetime, timezone
from re import sub

from sqlalchemy import Boolean, Column, DateTime
from sqlalchemy.dialects.postgresql.base import UUID
from sqlalchemy.ext.declarative import as_declarative, declared_attr


# Function to convert CamelCase to snake_case
def snake_case(s):
    """
    e.g. "SnakeCase" -> "snake_case"
    e.g. "Snake-Case" -> "snake_case"
    e.g. "SNAKECase" -> "snake_case"
    e.g. "snakeCase" -> "snake_case"
    e.g. "SnakeCASE" -> "snake_case"
    """
    return "_".join(
        sub(
            "([A-Z][a-z]+)", r" \1", sub("([A-Z]+)", r" \1", s.replace("-", " "))
        ).split()
    ).lower()


# Base class for ORM models with common columns
@as_declarative()
class Base:
    __name__: str

    ID = "id"
    IS_ACTIVE = "is_active"
    CREATED_AT = "created_at"
    UPDATED_AT = "updated_at"
    DELETED_AT = "deleted_at"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    is_active = Column(Boolean, default=True)
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )
    deleted_at = Column(DateTime(timezone=True), default=None)

    # Generate __tablename__ automatically from class name
    @declared_attr
    def __tablename__(cls) -> str:
        return snake_case(cls.__name__)


# Base class for ORM models without common columns but with dynamic table name
@as_declarative()
class BaseMTM:
    __name__: str

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Generate __tablename__ automatically from class name
    @declared_attr
    def __tablename__(cls) -> str:
        return snake_case(cls.__name__)