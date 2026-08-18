import time

import redis
from fastapi import HTTPException, Request

from app.core.config import get_settings

settings = get_settings()
_redis_client = redis.Redis.from_url(settings.redis_url, decode_responses=True)


def rate_limit(request: Request) -> None:
    """Fixed-window limiter keyed by client IP (SRS 3.4.4 - rate limiting
    on public prediction endpoints)."""
    window = int(time.time() // 60)
    key = f"ratelimit:{request.client.host if request.client else 'unknown'}:{window}"

    count = _redis_client.incr(key)
    if count == 1:
        _redis_client.expire(key, 60)

    if count > settings.prediction_rate_limit_per_minute:
        raise HTTPException(status_code=429, detail="Rate limit exceeded, try again shortly")
