import uuid
from typing import Any, Dict, List

from fastapi_mail import FastMail, MessageSchema

from constants.common import AppTranslationKeys
from core.email_connection import conf
from services.abstract.email_service import EmailService
from templates.utils import template_manager
from utils.logger import setup_logger


class EmailServiceImpl(EmailService):
    """
    Implementation of the EmailService for handling all email sending operations.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._logger = setup_logger()
        self._translation = AppTranslationKeys()

        # Create FastMail client
        self._mail_client = FastMail(conf)

    async def _send_email(
        self,
        subject: str,
        recipients: List[str],
        template_path: str,
        template_data: Dict[str, Any],
    ) -> bool:
        """
        Generic method to send emails.

        Args:
            subject: Email subject
            recipients: List of recipient email addresses
            template_path: Path to the HTML template
            template_data: Data to render in the template

        Returns:
            bool: True if email was sent successfully, False otherwise
        """
        try:
            # Add base_frontend_url to all templates by default
            if "base_frontend_url" not in template_data:
                template_data["base_frontend_url"] = conf.MAIL_FROM

            # Log template data for debugging
            self._logger.info(f"Attempting to render template: {template_path}")
            self._logger.info(f"Template data: {template_data}")

            # Render the HTML template
            html_content = template_manager.render_template(
                template_path, **template_data
            )

            # Create the message
            message = MessageSchema(
                subject=subject,
                recipients=recipients,
                body=html_content,
                subtype="html",
            )

            # Send the email
            await self._mail_client.send_message(message)
            self._logger.info(f"Email sent successfully to {recipients}")
            return True
        except Exception as e:
            self._logger.error(f"Error sending email to {recipients}: {str(e)}")
            # Print the full exception traceback for debugging
            import traceback

            self._logger.error(f"Exception details: {traceback.format_exc()}")
            return False

    async def send_verification_email(
        self, user_info: Dict[str, Any], code_number: str
    ) -> bool:
        """
        Send verification email to a user.

        Args:
            user_info: Dictionary containing user information
            code_number: Verification code

        Returns:
            bool: True if email was sent successfully, False otherwise
        """
        self._logger.info(f"Sending verification email to {user_info['email']}")
        return await self._send_email(
            subject="Verify Email Address for Adoor",
            recipients=[user_info["email"]],
            template_path="verification.html",
            template_data={
                "display_name": user_info["name"],
                "phone_number": user_info["phone_number"],
                "code_number": code_number,
            },
        )

    async def send_reset_password_email(
        self, email: str, password_reset: str, display_name: str
    ) -> bool:
        """
        Send reset password email to a user.

        Args:
            email: User's email address
            password_reset: Password reset token
            display_name: User's display name

        Returns:
            bool: True if email was sent successfully, False otherwise
        """
        self._logger.info(f"Sending password reset email to {email}")
        try:
            return await self._send_email(
                subject="Reset Your Password - Adoor",
                recipients=[email],
                template_path="reset_password.html",
                template_data={
                    "display_name": display_name,
                    "password_reset": password_reset,
                    "reset_url": f"{conf.MAIL_FROM_NAME}/reset-password?token={password_reset}",
                },
            )
        except Exception as e:
            self._logger.error(f"Failed to send password reset email: {str(e)}")
            return False

    async def send_invitation_with_password_email(
        self,
        email: str,
        password_user_invite: str,
        display_name: str,
        org_name: str,
        user_id: uuid.UUID,
    ) -> bool:
        """
        Send invitation with password to a user.

        Args:
            email: User's email address
            password_user_invite: Generated password for the user
            display_name: User's display name
            org_name: Organization name
            user_id: User ID

        Returns:
            bool: True if email was sent successfully, False otherwise
        """
        self._logger.info(f"Sending invitation email with password to {email}")
        return await self._send_email(
            subject=f"Invitation to join {org_name}",
            recipients=[email],
            template_path="invite_user.html",
            template_data={
                "display_name": display_name,
                "password_user_invite": password_user_invite,
                "org_name": org_name,
                "email": email,
                "user_id": user_id,
            },
        )

    async def send_invitation_organization(
        self, email: str, display_name: str, org_name: str
    ) -> bool:
        """
        Send organization invitation to a user.

        Args:
            email: User's email address
            display_name: User's display name
            org_name: Organization name

        Returns:
            bool: True if email was sent successfully, False otherwise
        """
        self._logger.info(f"Sending organization invitation to {email}")
        return await self._send_email(
            subject=f"Invitation to join {org_name}",
            recipients=[email],
            template_path="invite_user_no_credentials.html",
            template_data={"display_name": display_name, "org_name": org_name},
        )

    async def send_new_user_registration_email_to_ceo(
        self, email: str, display_name: str, phone_number: str, user_id: str
    ) -> bool:
        """
        Send notification email to CEO about new user registration.

        Args:
            email: User's email address
            display_name: User's display name
            phone_number: User's phone number
            user_id: User ID

        Returns:
            bool: True if email was sent successfully, False otherwise
        """
        self._logger.info(
            f"Sending new user registration notification to CEO: {conf.MAIL_FROM}"
        )
        return await self._send_email(
            subject="New User Registration Notification",
            recipients=[conf.MAIL_FROM],
            template_path="new_account_ceo.html",
            template_data={
                "email": email,
                "display_name": display_name,
                "phone_number": phone_number,
                "user_id": user_id,
            },
        )

    async def send_account_approved_email(self, email: str, display_name: str) -> bool:
        """
        Send account approval notification email to user.

        Args:
            email: User's email address
            display_name: User's display name

        Returns:
            bool: True if email was sent successfully, False otherwise
        """
        self._logger.info(f"Sending account approval notification to {email}")
        return await self._send_email(
            subject="Account Approved by Adoor",
            recipients=[email],
            template_path="account_approved.html",
            template_data={"display_name": display_name},
        )
