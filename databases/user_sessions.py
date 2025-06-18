from datetime import datetime

from databases.base.class_base import Base
from sqlalchemy import Column, DateTime, ForeignKey, Index, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship


class UserSessions(Base):
    __tablename__ = "user_sessions"

    """FK"""
    user_id = Column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    """Attributes"""
    refresh_token = Column(Text, nullable=False, unique=True, default="")
    expires_at = Column(DateTime(timezone=True), default=datetime.now, nullable=False)

    """Relationships"""
    user = relationship("Users", back_populates="user_sessions")

    # add index to user_id, refresh_token in the user_sessions table
    __table_args__ = (
        Index("idx_user_sessions_user_id", "user_id"),
        Index("idx_user_sessions_refresh_token", "refresh_token"),
    )
