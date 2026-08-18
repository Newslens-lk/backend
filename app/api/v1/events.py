from datetime import datetime
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.article import Article
from app.models.event import Event
from app.schemas.event import EventDetail, EventSummary

router = APIRouter(prefix="/events", tags=["events"])


@router.get("", response_model=list[EventSummary])
def list_events(
    date_from: datetime | None = None,
    date_to: datetime | None = None,
    limit: int = Query(default=20, le=100),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
) -> list[Event]:
    stmt = select(Event).order_by(Event.window_start.desc())
    if date_from is not None:
        stmt = stmt.where(Event.window_start >= date_from)
    if date_to is not None:
        stmt = stmt.where(Event.window_end <= date_to)
    stmt = stmt.limit(limit).offset(offset)
    return list(db.scalars(stmt))


@router.get("/{event_id}", response_model=EventDetail)
def get_event(event_id: UUID, db: Session = Depends(get_db)) -> EventDetail:
    event = db.get(Event, str(event_id))
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")

    articles = list(
        db.scalars(
            select(Article)
            .where(Article.event_id == str(event_id))
            .order_by(Article.published_at)
        )
    )
    return EventDetail(**EventSummary.model_validate(event).model_dump(), articles=articles)
