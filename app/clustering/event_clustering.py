def cluster_candidates(article_ids: list[int]) -> dict[int, int]:
    """Group candidate articles (already filtered to a time window, per
    FR1.3) into event clusters using HDBSCAN with Leiden refinement.

    Returns a mapping of article_id -> event_id (or a fresh noise-cluster
    id, per REQ-1.3.2/REQ-1.3.3). Requires requirements-ml.txt.
    """
    raise NotImplementedError("Implement HDBSCAN + Leiden clustering over article embeddings")


def assign_to_existing_or_new_cluster(article_id: int) -> int:
    """Incrementally place a newly ingested article into an existing
    event cluster, or start a new one (REQ-1.3.4)."""
    raise NotImplementedError("Implement nearest-cluster lookup via pgvector similarity search")
