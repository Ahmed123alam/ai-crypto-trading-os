"""Strategy endpoints."""
from fastapi import APIRouter, Depends
from backend.database import get_db_session
from backend.models import Strategy
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

router = APIRouter()


@router.get("")
async def get_strategies(session: AsyncSession = Depends(get_db_session)):
    """Get all strategies."""
    result = await session.execute(select(Strategy))
    strategies = result.scalars().all()
    
    return {"strategies": strategies, "count": len(strategies)}


@router.post("")
async def create_strategy(strategy_data: dict, session: AsyncSession = Depends(get_db_session)):
    """Create new strategy."""
    strategy = Strategy(**strategy_data)
    session.add(strategy)
    await session.commit()
    
    return {"strategy_id": strategy.id, "status": "created"}


@router.put("/{strategy_id}")
async def update_strategy(strategy_id: str, updates: dict, session: AsyncSession = Depends(get_db_session)):
    """Update strategy."""
    strategy = await session.get(Strategy, strategy_id)
    if not strategy:
        return {"error": "Strategy not found"}
    
    for key, value in updates.items():
        setattr(strategy, key, value)
    
    await session.commit()
    return {"strategy_id": strategy.id, "status": "updated"}
