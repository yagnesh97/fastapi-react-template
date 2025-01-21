from redis import Redis

from app.config import settings


def get_redis_client() -> Redis:  # type: ignore[type-arg]
    if settings.ci:
        from fakeredis import FakeStrictRedis

        return FakeStrictRedis(version=7, decode_responses=True)

    return Redis(
        host=settings.redis_host,
        port=settings.redis_port,
        db=0,
        password=settings.redis_password,
        decode_responses=True,
    )


redis_client = get_redis_client()
