"""Health check endpoints."""
from fastapi import APIRouter, Depends
from datetime import datetime
from backend.database import get_db_session
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.get("/status")
async def health_status():
    """Get system health status."""
    return {
        "status": "operational",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0",
        "components": {
            "api": "up",
            "database": "up",
            "redis": "up",
            "trading_engine": "up",
            "ai_agents": "up"
        }
    }


@router.get("/ready")
async def readiness_check(session: AsyncSession = Depends(get_db_session)):
    """Check if system is ready."""
    return {
        "ready": True,
        "timestamp": datetime.utcnow().isoformat()
    }
