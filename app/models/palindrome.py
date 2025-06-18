import uuid
from sqlalchemy import (
    Column,
    String,
    DateTime,
    Boolean,
    Index,
)
from app.extensions import db
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.sql import func


class Palindrome(db.Model):
    __tablename__ = "palindromes"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    text = Column(String(255), nullable=False)
    language = Column(String(2), nullable=False, index=True)
    is_palindrome = Column(Boolean, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    __table_args__ = (Index("idx_language", "language"),)

    def __repr__(self):
        return f"<Palindrome {self.text}>"
