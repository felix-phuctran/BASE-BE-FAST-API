import uuid
from abc import ABC, abstractmethod
from typing import Any, Dict, List

from pydantic import BaseModel, EmailStr


class EmailService(BaseModel, ABC):
    """
    Abstract base class for email service operations.
    """
    class Config:
        arbitrary_types_allowed = True
        extra = "allow"

    @abstractmethod
    async def _send_email(
        self,
        subject: str,
        recipients: List[EmailStr],
        template_path: str,
        template_data: Dict[str, Any]
    ) -> bool:
        """
        Abstract method for sending emails.
        
        Args:
            subject: Email subject
            recipients: List of recipient email addresses
            template_path: Path to the HTML template
            template_data: Data to render in the template
            
        Returns:
            bool: True if email was sent successfully, False otherwise
        """
        pass

    @abstractmethod
    async def send_verification_email(
        self, 
        user_info: Dict[str, Any], 
        code_number: str
    ) -> bool:
        """
        Send verification email to a user.
        
        Args:
            user_info: Dictionary containing user information
            code_number: Verification code
            
        Returns:
            bool: True if email was sent successfully, False otherwise
        """
        pass

    @abstractmethod
    async def send_reset_password_email(
        self, 
        email: EmailStr, 
        password_reset: str, 
        display_name: str
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
        pass

    @abstractmethod
    async def send_invitation_with_password_email(
        self, 
        email: EmailStr, 
        password_user_invite: str, 
        display_name: str, 
        org_name: str, 
        user_id: uuid.UUID
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
        pass

    @abstractmethod
    async def send_invitation_organization(
        self, 
        email: EmailStr, 
        display_name: str, 
        org_name: str
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
        pass

    @abstractmethod
    async def send_new_user_registration_email_to_ceo(
        self, 
        email: EmailStr, 
        display_name: str, 
        phone_number: str, 
        user_id: str
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
        pass

    @abstractmethod
    async def send_account_approved_email(
        self, 
        email: EmailStr, 
        display_name: str
    ) -> bool:
        """
        Send account approval notification email to user.
        
        Args:
            email: User's email address
            display_name: User's display name
            
        Returns:
            bool: True if email was sent successfully, False otherwise
        """
        pass
