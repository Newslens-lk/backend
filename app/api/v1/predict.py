from fastapi import APIRouter, Depends

from app.classification.classifier import predict_bias
from app.core.rate_limit import rate_limit
from app.preprocessing.cleaning import clean_text, fetch_and_clean_url
from app.schemas.prediction import PredictionRequest, PredictionResponse

router = APIRouter(prefix="/predict", tags=["predict"])


@router.post("", response_model=PredictionResponse, dependencies=[Depends(rate_limit)])
def predict_article_bias(payload: PredictionRequest) -> PredictionResponse:
    text = clean_text(payload.text) if payload.text else fetch_and_clean_url(str(payload.url))
    return predict_bias(text)
