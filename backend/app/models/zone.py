from sqlalchemy import String, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.session import Base
import uuid


class Zone(Base):
    __tablename__ = "zones"
    id:        Mapped[str] = mapped_column(String, primary_key=True,
                                           default=lambda: str(uuid.uuid4()))
    camera_id: Mapped[str] = mapped_column(ForeignKey("cameras.id"))
    name:      Mapped[str] = mapped_column(String)
    polygon:   Mapped[list] = mapped_column(JSON)  # normalised [[x,y], ...]

    camera: Mapped["Camera"] = relationship(back_populates="zones")
