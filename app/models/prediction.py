from datetime import datetime

from sqlalchemy import ARRAY, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Prediction(Base):
    __tablename__ = "predictions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    article_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("articles.id", ondelete="CASCADE"), index=True
    )
    model_version: Mapped[str] = mapped_column(String(50))

    dimension_a_label: Mapped[str] = mapped_column(String(50))
    dimension_a_confidence: Mapped[float] = mapped_column(Float)
    dimension_b_labels: Mapped[list[str]] = mapped_column(ARRAY(String))
    dimension_b_confidences: Mapped[list[float]] = mapped_column(ARRAY(Float))

    predicted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
