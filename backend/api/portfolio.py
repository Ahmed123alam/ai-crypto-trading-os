"""Portfolio endpoints."""
from fastapi import APIRouter, Depends
from backend.database import get_db_session
from backend.models import Portfolio, Position, Trade
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

router = APIRouter()


@router.get("")
async def get_portfolio(session: AsyncSession = Depends(get_db_session)):
    """Get portfolio summary."""
    result = await session.execute(select(Portfolio).limit(1))
    portfolio = result.scalar()
    
    if not portfolio:
        return {"message": "No portfolio found"}
    
    return {
        "id": portfolio.id,
        "total_balance": portfolio.total_balance,
        "available_balance": portfolio.available_balance,
        "unrealized_pnl": portfolio.unrealized_pnl,
        "realized_pnl": portfolio.realized_pnl,
    }


@router.get("/positions")
async def get_positions(session: AsyncSession = Depends(get_db_session)):
    """Get open positions."""
    result = await session.execute(select(Position))
    positions = result.scalars().all()
    
    return {"positions": positions, "count": len(positions)}


@router.get("/performance")
async def get_performance(session: AsyncSession = Depends(get_db_session)):
    """Get portfolio performance metrics."""
    result = await session.execute(select(Trade).order_by(Trade.created_at))
    trades = result.scalars().all()
    
    total_trades = len(trades)
    winning_trades = sum(1 for t in trades if t.pnl > 0 and t.status == "CLOSED")
    losing_trades = sum(1 for t in trades if t.pnl < 0 and t.status == "CLOSED")
    total_pnl = sum(t.pnl for t in trades if t.status == "CLOSED")
    
    win_rate = (winning_trades / (winning_trades + losing_trades) * 100) if (winning_trades + losing_trades) > 0 else 0
    
    return {
        "total_trades": total_trades,
        "winning_trades": winning_trades,
        "losing_trades": losing_trades,
        "win_rate": win_rate,
        "total_pnl": total_pnl,
    }
