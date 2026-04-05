from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.session import Base
import uuid


class Organization(Base):
    __tablename__ = "organizations"
    id:   Mapped[str] = mapped_column(String, primary_key=True,
                                      default=lambda: str(uuid.uuid4()))
    name: Mapped[str] = mapped_column(String, nullable=False)
    stores: Mapped[list["Store"]] = relationship(back_populates="organization")
