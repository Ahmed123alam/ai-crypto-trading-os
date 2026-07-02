"""Database configuration and initialization."""
import logging
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from motor.motor_asyncio import AsyncIOMotorClient
import aioredis

from backend.config import settings

logger = logging.getLogger(__name__)

# SQLAlchemy
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    pool_size=20,
    max_overflow=0,
)

AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

Base = declarative_base()

# MongoDB
mongo_client: AsyncIOMotorClient = None
mongo_db = None

# Redis
redis_client = None


async def init_db():
    """Initialize all databases."""
    global mongo_client, mongo_db, redis_client
    
    # PostgreSQL
    logger.info("Initializing PostgreSQL...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("✅ PostgreSQL initialized")
    
    # MongoDB
    logger.info("Initializing MongoDB...")
    mongo_client = AsyncIOMotorClient(settings.MONGODB_URL)
    mongo_db = mongo_client["crypto_trading"]
    logger.info("✅ MongoDB initialized")
    
    # Redis
    logger.info("Initializing Redis...")
    redis_client = await aioredis.from_url(
        settings.REDIS_URL,
        encoding="utf8",
        decode_responses=True,
    )
    logger.info("✅ Redis initialized")


async def close_db():
    """Close all database connections."""
    await engine.dispose()
    if mongo_client:
        mongo_client.close()
    if redis_client:
        await redis_client.close()


async def get_db_session() -> AsyncSession:
    """Get database session."""
    async with AsyncSessionLocal() as session:
        yield session
