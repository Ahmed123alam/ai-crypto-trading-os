"""Trade management endpoints."""
from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime
from backend.database import get_db_session
from backend.models import Trade
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

router = APIRouter()


@router.get("")
async def get_trades(session: AsyncSession = Depends(get_db_session)):
    """Get all trades."""
    result = await session.execute(select(Trade).order_by(Trade.created_at.desc()))
    trades = result.scalars().all()
    return {"trades": trades, "count": len(trades)}


@router.get("/{trade_id}")
async def get_trade(trade_id: str, session: AsyncSession = Depends(get_db_session)):
    """Get specific trade."""
    trade = await session.get(Trade, trade_id)
    if not trade:
        raise HTTPException(status_code=404, detail="Trade not found")
    return trade


@router.post("")
async def create_trade(trade_data: dict, session: AsyncSession = Depends(get_db_session)):
    """Create new trade."""
    trade = Trade(**trade_data)
    session.add(trade)
    await session.commit()
    return {"trade_id": trade.id, "status": "created"}


@router.post("/{trade_id}/close")
async def close_trade(trade_id: str, session: AsyncSession = Depends(get_db_session)):
    """Close a trade."""
    trade = await session.get(Trade, trade_id)
    if not trade:
        raise HTTPException(status_code=404, detail="Trade not found")
    
    trade.status = "CLOSED"
    trade.closed_at = datetime.utcnow()
    await session.commit()
    
    return {"trade_id": trade.id, "status": "closed"}
