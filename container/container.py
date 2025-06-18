# Standard library imports
from typing import Any, Dict

# Models
from databases.user_sessions import UserSessions
from databases.users import Users

# Third-party imports
from redis import asyncio as aioredis

# Application constants
from constants.common import AppTranslationKeys
from config.env import Env

# Repositories - ORM
from repositories.orm.orm_crud_user import ORMCRUDUser
from repositories.orm.orm_crud_user_session import ORMCRUDUserSession

# Services - Abstract
from services.abstract.email_service import EmailService
from services.abstract.user_management_service import UserManagementService

# Services - Implementation
from services.implement.email_service_impl import EmailServiceImpl
from services.implement.user_management_service_impl import UserManagementServiceImpl

# Import utilities and config
from utils.logger import setup_logger


class Container:
    """Container for dependency injection"""

    _instance = None
    _repositories = {}
    _services = {}
    _utils = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Container, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        """Initialize all dependencies"""
        # Initialize utilities
        self._utils["logger"] = setup_logger()
        self._utils["env"] = Env()
        self._utils["translation"] = AppTranslationKeys()

        # Initialize repositories
        self._repositories["user"] = ORMCRUDUser(Users)
        self._repositories["user_session"] = ORMCRUDUserSession(UserSessions)

        # Initialize email service
        self._services["email"] = EmailServiceImpl(
            logger=self._utils["logger"], translation=self._utils["translation"]
        )

        # Initialize Redis client
        redis_url = self._utils["env"].REDIS_URL
        self._utils["redis"] = aioredis.from_url(
            redis_url, encoding="utf-8", decode_responses=True
        )

        # Initialize user management service
        self._services["user_management"] = UserManagementServiceImpl(
            logger=self._utils["logger"],
            translation=self._utils["translation"],
            orm_crud_user=self._repositories["user"],
        )

    def get_repository(self, name: str) -> Any:
        """Get a repository by name"""
        return self._repositories.get(name)

    def get_service(self, name: str) -> Any:
        """Get a service by name"""
        return self._services.get(name)

    def get_util(self, name: str) -> Any:
        """Get a utility by name"""
        return self._utils.get(name)

    def get_email_service(self) -> EmailService:
        """Get email service with proper type annotation"""
        return self._services["email"]

    def get_user_management_service(self) -> UserManagementService:
        """Get user management service with proper type annotation"""
        return self._services["user_management"]


# Create a singleton instance
container = Container()
