from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.schemas.article import ArticleOut


class EventSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    summary: str | None
    started_at: datetime
    article_count: int


class EventDetail(EventSummary):
    articles: list[ArticleOut] = []
