"""Database initialization script."""
import asyncio
import logging
from backend.database import init_db, mongo_db, redis_client
from backend.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def init_indexes():
    """Initialize database indexes."""
    # MongoDB indexes
    if mongo_db:
        await mongo_db['trades'].create_index('user_id')
        await mongo_db['trades'].create_index('created_at')
        await mongo_db['signals'].create_index('timestamp')
        logger.info("✅ MongoDB indexes created")
    
    # Redis keys
    if redis_client:
        await redis_client.set('system:status', 'initialized')
        logger.info("✅ Redis initialized")


async def main():
    """Initialize all systems."""
    logger.info("🚀 Initializing databases...")
    await init_db()
    await init_indexes()
    logger.info("✅ All systems initialized")


if __name__ == "__main__":
    asyncio.run(main())
