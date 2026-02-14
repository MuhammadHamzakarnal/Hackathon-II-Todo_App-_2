from datetime import datetime
from typing import Optional, TYPE_CHECKING
from sqlmodel import Field, SQLModel, Relationship

if TYPE_CHECKING:
    from .user import User


class Log(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    timestamp: datetime = Field(default_factory=datetime.utcnow, index=True)
    action: str = Field(index=True)
    details: Optional[str] = Field(default=None)

    user_id: int = Field(foreign_key="users.id", index=True)
    user: "User" = Relationship(back_populates="logs")
