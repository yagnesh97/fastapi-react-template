from datetime import datetime, timedelta, timezone

from fastapi.responses import JSONResponse

from app.utilities.redis import redis_client
from app.utilities.static_values import RATE_LIMIT_EXCEED


async def rate_limit_ip(ip: str, rate_limit: int) -> JSONResponse | None:
    """
    Apply rate limiting per IP address, per minute
    """
    # Increment the most recent redis key based on IP address
    now = datetime.now(tz=timezone.utc)
    current_minute = now.strftime("%Y-%m-%dT%H:%M")

    redis_key = f"rate_limit_{ip}_{current_minute}"
    current_count = redis_client.incr(redis_key)

    # If it's the first request, set an expiration time
    if current_count == 1:
        redis_client.expireat(name=redis_key, when=now + timedelta(minutes=1))

    # Check if the rate limit has been exceeded
    if current_count > rate_limit + 1:
        return JSONResponse(
            status_code=429,
            content={"detail": RATE_LIMIT_EXCEED},
            headers={
                "Retry-After": f"{60 - now.second}",
                "X-Rate-Limit": f"{rate_limit}",
            },
        )

    return None
