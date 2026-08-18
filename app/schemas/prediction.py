from pydantic import BaseModel, ConfigDict, HttpUrl, model_validator


class PredictionRequest(BaseModel):
    text: str | None = None
    url: HttpUrl | None = None

    @model_validator(mode="after")
    def require_text_or_url(self) -> "PredictionRequest":
        if not self.text and not self.url:
            raise ValueError("either 'text' or 'url' must be provided")
        return self


class PredictionResponse(BaseModel):
    model_config = ConfigDict(protected_namespaces=())

    dimension_a_label: str
    dimension_a_confidence: float
    dimension_b_labels: list[str]
    dimension_b_confidences: list[float]
    model_version: str
    nearest_event_id: int | None = None
