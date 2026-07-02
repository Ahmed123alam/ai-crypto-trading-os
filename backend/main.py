"""Main FastAPI application entry point."""
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware

from backend.api import health, trades, portfolio, agents, strategies
from backend.config import settings
from backend.database import init_db
from backend.websocket import WebSocketManager
from backend.trading_engine import init_trading_engine
from backend.ai_agents import init_agents

logging.basicConfig(level=settings.LOG_LEVEL)
logger = logging.getLogger(__name__)

# Global instances
ws_manager = WebSocketManager()
trading_engine = None
ai_agents = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize and cleanup on startup/shutdown."""
    logger.info("🚀 Starting AI Crypto Trading Operating System...")
    
    # Startup
    await init_db()
    global trading_engine, ai_agents
    trading_engine = await init_trading_engine()
    ai_agents = await init_agents()
    logger.info("✅ All systems initialized")
    
    yield
    
    # Shutdown
    logger.info("🛑 Shutting down...")
    if trading_engine:
        await trading_engine.shutdown()
    if ai_agents:
        await ai_agents.shutdown()
    logger.info("✅ Shutdown complete")


app = FastAPI(
    title="AI Crypto Trading OS",
    description="Institutional-grade AI crypto trading operating system",
    version="1.0.0",
    lifespan=lifespan
)

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Routes
app.include_router(health.router, prefix="/api/health", tags=["health"])
app.include_router(trades.router, prefix="/api/trades", tags=["trades"])
app.include_router(portfolio.router, prefix="/api/portfolio", tags=["portfolio"])
app.include_router(agents.router, prefix="/api/agents", tags=["agents"])
app.include_router(strategies.router, prefix="/api/strategies", tags=["strategies"])


@app.websocket("/ws")
async def websocket_endpoint(websocket):
    """WebSocket endpoint for real-time data streaming."""
    await ws_manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await ws_manager.broadcast(data)
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
    finally:
        await ws_manager.disconnect(websocket)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.FASTAPI_HOST,
        port=settings.FASTAPI_PORT,
        reload=settings.DEBUG,
        workers=settings.WORKERS,
    )
