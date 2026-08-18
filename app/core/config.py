from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    environment: str = "development"

    database_url: str = "postgresql+psycopg://newslens:newslens@localhost:5432/newslens"
    redis_url: str = "redis://localhost:6379/0"

    api_v1_prefix: str = "/api/v1"
    cors_origins: str = "http://localhost:3000"

    # Configurable pipeline values (SRS 3.5.3) - kept out of code so they
    # can be tuned without a redeploy.
    min_article_length: int = 200
    clustering_time_window_hours: int = 72
    scheduled_ingestion_interval_minutes: int = 30

    prediction_rate_limit_per_minute: int = 10

    @property
    def cors_origin_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
