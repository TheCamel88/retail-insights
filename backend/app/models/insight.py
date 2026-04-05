from sqlalchemy import String, DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.db.session import Base
from datetime import datetime
import uuid


class Insight(Base):
    __tablename__ = "insights"
    id:          Mapped[str]      = mapped_column(String, primary_key=True,
                                                  default=lambda: str(uuid.uuid4()))
    store_id:    Mapped[str]      = mapped_column(String, index=True)
    period_start: Mapped[datetime] = mapped_column(DateTime)
    period_end:   Mapped[datetime] = mapped_column(DateTime)
    summary:     Mapped[str]      = mapped_column(Text)      # AI-generated text
    created_at:  Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
