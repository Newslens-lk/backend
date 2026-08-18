import uuid
from datetime import UTC, datetime, timedelta

import pytest
from fastapi.testclient import TestClient

from app.db.session import SessionLocal
from app.main import app
from app.models.article import Article
from app.models.event import Event
from app.models.source import Source

client = TestClient(app)


@pytest.fixture
def seeded_event() -> uuid.UUID:
    event_id = uuid.uuid4()
    now = datetime.now(UTC)
    source_name = f"test-source-{event_id.hex[:8]}"
    article_id = f"test-article-{event_id.hex[:8]}"

    db = SessionLocal()
    try:
        db.add(Source(source_name=source_name, source_type="html"))
        db.commit()

        db.add(
            Event(
                event_id=str(event_id),
                summary=None,
                topic=None,
                article_count=1,
                source_count=1,
                window_start=now - timedelta(hours=1),
                window_end=now,
            )
        )
        db.commit()

        db.add(
            Article(
                article_id=article_id,
                source_name=source_name,
                url=f"https://example.com/{article_id}",
                title="Test headline",
                body="Test body content",
                language="si",
                published_at=now,
                event_id=str(event_id),
            )
        )
        db.commit()
        yield event_id
    finally:
        db.query(Article).filter(Article.article_id == article_id).delete()
        db.query(Event).filter(Event.event_id == str(event_id)).delete()
        db.query(Source).filter(Source.source_name == source_name).delete()
        db.commit()
        db.close()


def test_list_events_returns_seeded_event(seeded_event: uuid.UUID) -> None:
    response = client.get("/api/v1/events")
    assert response.status_code == 200
    ids = [row["event_id"] for row in response.json()]
    assert str(seeded_event) in ids


def test_get_event_includes_articles(seeded_event: uuid.UUID) -> None:
    response = client.get(f"/api/v1/events/{seeded_event}")
    assert response.status_code == 200
    body = response.json()
    assert body["event_id"] == str(seeded_event)
    assert len(body["articles"]) == 1
    assert body["articles"][0]["title"] == "Test headline"


def test_get_event_not_found() -> None:
    response = client.get(f"/api/v1/events/{uuid.uuid4()}")
    assert response.status_code == 404


def test_list_articles_filters_by_source(seeded_event: uuid.UUID) -> None:
    db = SessionLocal()
    try:
        article = db.query(Article).filter(Article.event_id == str(seeded_event)).one()
    finally:
        db.close()

    response = client.get("/api/v1/articles", params={"source_name": article.source_name})
    assert response.status_code == 200
    assert all(row["source_name"] == article.source_name for row in response.json())


def test_get_article_not_found() -> None:
    response = client.get("/api/v1/articles/does-not-exist")
    assert response.status_code == 404
