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
    await token_blocklist.set(name=jti, value="", ex=JTI_EXPIRY)


async def token_in_blocklist(jti: str) -> bool:  # check if the token is in the blocklist
    val = await token_blocklist.get(name=jti)
    return val is not None