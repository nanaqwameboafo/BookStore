import logging
import redis.asyncio as redis
from src.config import Config

JTI_EXPIRY = 3600

# Use the maintained `redis` package asyncio client instead of aioredis
token_blocklist = redis.Redis(
    host=Config.REDIS_HOST,
    port=Config.REDIS_PORT,
    db=0,
)


async def add_token_to_blocklist(jti: str) -> None:  # add token to the block list
    try:
        await token_blocklist.set(name=jti, value="", ex=JTI_EXPIRY)
    except Exception as e:
        # Log and continue — failing to write to Redis should not crash the app
        logging.error(f"Failed to add token to Redis blocklist: {e}")


async def token_in_blocklist(jti: str) -> bool:  # check if the token is in the blocklist
    try:
        val = await token_blocklist.get(name=jti)
        return val is not None
    except Exception as e:
        # If Redis is down/unreachable, log the error and treat token as not blocked
        logging.error(f"Failed to read token blocklist from Redis: {e}")
        return False