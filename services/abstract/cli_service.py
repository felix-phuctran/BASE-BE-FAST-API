import uuid
from abc import ABC, abstractmethod
from typing import Any, Dict, List

from pydantic import BaseModel
from sqlalchemy.orm import Session


class CliService(ABC):
    """Abstract base class for CLI service operations."""

    @abstractmethod
    async def _initialize_db(self) -> str:
        """
        Abstract method for executing a command in the CLI.

        Returns:
            str: The output of the command execution
        """
        pass

    @abstractmethod
    async def _initialize_user(self, db_session: Session) -> str:
        """
        Abstract method for initializing a supplier in the CLI.
        This method should handle the setup and initialization of supplier-specific configurations.

        Returns:
            str: The result or status message of the supplier initialization
        """
        pass
