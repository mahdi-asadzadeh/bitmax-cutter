from sqlalchemy import Column
from sqlalchemy.sql import func
from sqlalchemy.types import Integer, Text, String, DateTime
from bitmax_cutter.models.database import Base


class User(Base):
    """User account."""

    __tablename__ = "user"
    id = Column(Integer, primary_key=True, autoincrement="auto", index=True)
    first_name = Column(String(255))
    last_name = Column(String(255))
    username = Column(String(255), unique=True, nullable=False)
    password = Column(Text, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now())

    def __repr__(self):
        return f"<User {self.username}>"
