from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class AssignRoleSchema(BaseModel):
    user_id: UUID
