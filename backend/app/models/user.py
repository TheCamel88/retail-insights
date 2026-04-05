from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from app.db.session import Base
import uuid


class User(Base):
    __tablename__ = "users"
    id:              Mapped[str]  = mapped_column(String, primary_key=True,
                                                  default=lambda: str(uuid.uuid4()))
    email:           Mapped[str]  = mapped_column(String, unique=True, nullable=False)
    hashed_password: Mapped[str]  = mapped_column(String, nullable=False)
    organization_id: Mapped[str]  = mapped_column(String, nullable=True)
    is_active:       Mapped[bool] = mapped_column(Boolean, default=True)
