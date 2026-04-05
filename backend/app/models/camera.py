from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.session import Base
import uuid


class Camera(Base):
    __tablename__ = "cameras"
    id:       Mapped[str] = mapped_column(String, primary_key=True,
                                          default=lambda: str(uuid.uuid4()))
    store_id: Mapped[str] = mapped_column(ForeignKey("stores.id"))
    name:     Mapped[str] = mapped_column(String)

    store: Mapped["Store"] = relationship(back_populates="cameras")
    zones: Mapped[list["Zone"]] = relationship(back_populates="camera")
