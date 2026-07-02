"""AI Agent endpoints."""
from fastapi import APIRouter, Depends
from datetime import datetime
from backend.database import get_db_session
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.get("")
async def get_agents():
    """Get all AI agents status."""
    return {
        "agents": [
            {
                "name": "Momentum Scalper",
                "status": "active",
                "win_rate": 0.52,
                "trades_today": 12
            },
            {
                "name": "Order Flow AI",
                "status": "active",
                "win_rate": 0.48,
                "trades_today": 8
            },
            {
                "name": "Mean Reversion AI",
                "status": "active",
                "win_rate": 0.55,
                "trades_today": 15
            },
            {
                "name": "Sentiment AI",
                "status": "active",
                "win_rate": 0.50,
                "trades_today": 5
            },
            {
                "name": "Whale Tracker",
                "status": "active",
                "win_rate": 0.60,
                "trades_today": 3
            },
        ]
    }


@router.get("/signals")
async def get_agent_signals():
    """Get current signals from all agents."""
    return {
        "timestamp": datetime.utcnow().isoformat(),
        "signals": [
            {
                "agent": "Momentum Scalper",
                "action": "BUY",
                "symbol": "BTC/USDT",
                "confidence": 0.78,
                "reason": "Volume expansion + RSI acceleration"
            },
            {
                "agent": "Whale Tracker",
                "action": "NEUTRAL",
                "symbol": "ETH/USDT",
                "confidence": 0.45,
                "reason": "Mixed whale movements"
            },
        ]
    }


@router.get("/{agent_name}/performance")
async def get_agent_performance(agent_name: str):
    """Get specific agent performance metrics."""
    return {
        "agent": agent_name,
        "total_trades": 42,
        "winning_trades": 22,
        "losing_trades": 20,
        "win_rate": 0.524,
        "profit_factor": 1.45,
        "avg_trade_duration": "2.5m",
        "best_trade": 125.50,
        "worst_trade": -85.25,
    }
