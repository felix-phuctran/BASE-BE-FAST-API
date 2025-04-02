from sqlalchemy import Boolean, Column, ForeignKey, Index, String, Text
from sqlalchemy.dialects.postgresql.base import UUID
from sqlalchemy.orm import relationship

from models.base.class_base import Base


class Users(Base):
    __tablename__ = "users"

    """FK"""
    # role_id = Column(UUID(as_uuid=True), ForeignKey("roles.id", ondelete="CASCADE"), nullable=False)
    # department_id = Column(UUID(as_uuid=True), ForeignKey("departments.id", ondelete="SET NULL"), nullable=True)
    """Attributes"""
    display_name = Column(String(255), nullable=False, default="user")
    password_hash = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    phone_number = Column(String(255), unique=True, nullable=True)
    avatar_url = Column(Text, nullable=True)
    is_verified = Column(Boolean, default=False, nullable=False)
    verification_code = Column(String(255), nullable=True)

    """Relationships"""
    user_sessions = relationship("UserSessions", back_populates="user")
    # role = relationship("Roles", back_populates="users")

    # add index to role_id, org_id, email, phone_number, is_verified in the users table
    __table_args__ = (
        # Index("ix_users_role_id", "role_id"),
        Index("ix_users_email", "email"),
        Index("ix_users_phone_number", "phone_number"),
        Index("ix_users_is_verified", "is_verified"),
    )
