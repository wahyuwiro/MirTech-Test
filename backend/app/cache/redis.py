import redis
import os

redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")

r = redis.Redis.from_url(redis_url, decode_responses=True)

def get_cached(key: str):
    return r.get(key)

def set_cached(key: str, value: str, ttl: int = 60):
    r.setex(key, ttl, value)
