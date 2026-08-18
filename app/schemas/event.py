from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.schemas.article import ArticleOut


class EventSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    event_id: UUID
    summary: str | None
    topic: str | None
    article_count: int
    source_count: int
    window_start: datetime | None
    window_end: datetime | None


class EventDetail(EventSummary):
    articles: list[ArticleOut] = []
