from datetime import datetime

from sqlalchemy import text
from sqlalchemy.orm import Session

from constants.common import AppTranslationKeys
from models.users import Users
from services.abstract.cli_service import CliService
from utils import hash
from utils.logger import setup_logger


class CliServiceImpl(CliService):
    """Implementation of the CLIService for handling all CLI operations."""

    def __init__(self, db_session: Session):
        self._logger = setup_logger()
        self._translation = AppTranslationKeys()
        self._db = db_session

    async def _initialize_db(self) -> str:
        """
        Initialize the database by executing a CLI command.

        Returns:
            str: The output of the command execution
        """
        self._logger.info("Initializing database...")
        # Here you would implement the actual logic to initialize the database
        # For example, running a shell command or using a library to set up the DB
        return "Database initialized successfully."

    async def _initialize_user(self, db_session: Session) -> str:
        """
        Initialize a user by executing a CLI command.

        Returns:
            str: The output of the command execution
        """

        mock_users = [
            {
                "id": "223e4567-e89b-12d3-a456-426614174017",
                "display_name": "admin",
                "email": "admin@gmail.com",
                "password_hash": hash("Allyai123456@"),
                "avatar_url": "https://frontend-assistain-ai-chatbot.vercel.app/logo/default_image_user.svg",
                "is_verified": True,
                "phone_number": "0123456789",
                "verification_code": "0000",
            }
        ]

        users = []
        for item in mock_users:
            user = Users(
                id=item["id"],
                display_name=item["display_name"],
                email=item["email"],
                password_hash=item["password_hash"],
                avatar_url=item["avatar_url"],
                is_verified=item["is_verified"],
                phone_number=item["phone_number"],
                verification_code=item["verification_code"],
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
                deleted_at=None,
                is_active=True,
            )
            users.append(user)

        try:
            # 1️⃣ Delete old data and reset ID
            await self._db.execute(
                text("TRUNCATE TABLE users RESTART IDENTITY CASCADE")
            )

            # 2️⃣ Insert new data into users table (using bulk_save_objects)
            self._db.add_all(users)
            await self._db.commit()

            # 3️⃣ Update sequence ID using ORDER BY for UUID

            await self._db.commit()

            print("[CLI] Created users successfully.")

            return "[CLI] Created users successfully."

        except Exception as e:
            await self._db.rollback()  # Rollback if error occurs
            print(f"[CLI] Error: {e}")
            return e

        return None  # Return None if successful
