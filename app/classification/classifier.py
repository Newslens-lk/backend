from app.schemas.prediction import PredictionResponse

MODEL_VERSION = "unset"


def predict_bias(article_text: str) -> PredictionResponse:
    """Run the trained Dimension A/B classifier on unseen article text
    and return labels with confidence scores (FR1.5). Requires a trained
    model artifact and requirements-ml.txt to be installed.
    """
    raise NotImplementedError(
        "Load the trained classifier (see requirements-ml.txt) and score the article text"
    )
