from app.models.embedding import LASER3_DIMENSION


def embed_text(text: str) -> list[float]:
    """Generate a LASER3 sentence embedding for the given article text
    (FR1.3 / REQ-1.3.1). Requires requirements-ml.txt to be installed.

    Loads the LASER3 model lazily so the base API can start without the
    heavy ML dependencies installed.
    """
    raise NotImplementedError(
        f"Load LASER3 and return a {LASER3_DIMENSION}-dim embedding for the article text"
    )
