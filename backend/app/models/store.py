from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.session import Base
import uuid


class Store(Base):
    __tablename__ = "stores"
    id:              Mapped[str] = mapped_column(String, primary_key=True,
                                                 default=lambda: str(uuid.uuid4()))
    organization_id: Mapped[str] = mapped_column(ForeignKey("organizations.id"))
    name:            Mapped[str] = mapped_column(String)
    address:         Mapped[str] = mapped_column(String, nullable=True)

    organization: Mapped["Organization"] = relationship(back_populates="stores")
    cameras:      Mapped[list["Camera"]] = relationship(back_populates="store")
