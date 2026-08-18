def summarize_event(article_bodies: list[str]) -> str:
    """Produce a single neutral Sinhala summary from all articles in an
    event cluster (FR1.4). Requires requirements-ml.txt.
    """
    raise NotImplementedError("Implement multi-document Sinhala summarization")


def fallback_title(earliest_article_title: str) -> str:
    """Used when summarization fails for a cluster (SRS 3.3.2 degraded
    mode: fall back to the earliest article's title)."""
    return earliest_article_title
