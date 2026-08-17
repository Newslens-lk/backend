"""initial schema

Revision ID: 0001
Revises:
Create Date: 2026-08-17

"""
from collections.abc import Sequence

import pgvector.sqlalchemy
import sqlalchemy as sa
from alembic import op

revision: str = "0001"
down_revision: str | None = None
branch_labels: Sequence[str] | None = None
depends_on: Sequence[str] | None = None

LASER3_DIMENSION = 1024


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")

    op.create_table(
        "articles",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("title", sa.Text(), nullable=False),
        sa.Column("body", sa.Text(), nullable=False),
        sa.Column("publisher", sa.String(255), nullable=False),
        sa.Column("url", sa.Text(), nullable=False),
        sa.Column("source_dataset", sa.String(100), nullable=False),
        sa.Column("published_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("collected_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("url", name="uq_articles_url"),
    )
    op.create_index("ix_articles_publisher", "articles", ["publisher"])
    op.create_index("ix_articles_published_at", "articles", ["published_at"])

    op.create_table(
        "embeddings",
        sa.Column(
            "article_id",
            sa.Integer(),
            sa.ForeignKey("articles.id", ondelete="CASCADE"),
            primary_key=True,
        ),
        sa.Column("vector", pgvector.sqlalchemy.Vector(LASER3_DIMENSION), nullable=False),
    )
    op.execute(
        "CREATE INDEX ix_embeddings_vector ON embeddings "
        "USING ivfflat (vector vector_cosine_ops) WITH (lists = 100)"
    )

    op.create_table(
        "events",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("title", sa.Text(), nullable=False),
        sa.Column("summary", sa.Text(), nullable=True),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("article_count", sa.Integer(), nullable=False, server_default="0"),
    )
    op.create_index("ix_events_started_at", "events", ["started_at"])

    op.create_table(
        "article_event",
        sa.Column(
            "article_id",
            sa.Integer(),
            sa.ForeignKey("articles.id", ondelete="CASCADE"),
            primary_key=True,
        ),
        sa.Column(
            "event_id",
            sa.Integer(),
            sa.ForeignKey("events.id", ondelete="CASCADE"),
            primary_key=True,
        ),
        sa.Column("membership_score", sa.Float(), nullable=False),
    )
    op.create_index("ix_article_event_event_id", "article_event", ["event_id"])

    op.create_table(
        "annotations",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "article_id", sa.Integer(), sa.ForeignKey("articles.id", ondelete="CASCADE")
        ),
        sa.Column("annotator_id", sa.String(100), nullable=False),
        sa.Column("dimension_a_label", sa.String(50), nullable=False),
        sa.Column("dimension_b_labels", sa.ARRAY(sa.String()), nullable=False),
        sa.Column("is_adjudicated", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_annotations_article_id", "annotations", ["article_id"])

    op.create_table(
        "predictions",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "article_id", sa.Integer(), sa.ForeignKey("articles.id", ondelete="CASCADE")
        ),
        sa.Column("model_version", sa.String(50), nullable=False),
        sa.Column("dimension_a_label", sa.String(50), nullable=False),
        sa.Column("dimension_a_confidence", sa.Float(), nullable=False),
        sa.Column("dimension_b_labels", sa.ARRAY(sa.String()), nullable=False),
        sa.Column("dimension_b_confidences", sa.ARRAY(sa.Float()), nullable=False),
        sa.Column("predicted_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_predictions_article_id", "predictions", ["article_id"])

    op.create_table(
        "outlet_stats",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("event_id", sa.Integer(), sa.ForeignKey("events.id", ondelete="CASCADE")),
        sa.Column("publisher", sa.String(255), nullable=False),
        sa.Column("covered", sa.Boolean(), nullable=False),
        sa.Column("reporting_latency_minutes", sa.Float(), nullable=True),
        sa.Column("lexical_stats", sa.JSON(), nullable=False, server_default="{}"),
        sa.Column("entity_stats", sa.JSON(), nullable=False, server_default="{}"),
    )
    op.create_index("ix_outlet_stats_event_id", "outlet_stats", ["event_id"])
    op.create_index("ix_outlet_stats_publisher", "outlet_stats", ["publisher"])


def downgrade() -> None:
    op.drop_table("outlet_stats")
    op.drop_table("predictions")
    op.drop_table("annotations")
    op.drop_table("article_event")
    op.drop_table("events")
    op.drop_table("embeddings")
    op.drop_table("articles")
    op.execute("DROP EXTENSION IF EXISTS vector")
