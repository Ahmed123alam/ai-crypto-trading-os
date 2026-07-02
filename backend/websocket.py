"""WebSocket Manager for real-time data streaming."""
import logging
import json
from typing import List, Set
from fastapi import WebSocket
from datetime import datetime

logger = logging.getLogger(__name__)


class WebSocketManager:
    """Manages WebSocket connections for real-time updates."""
    
    def __init__(self):
        self.active_connections: Set[WebSocket] = set()
        self.message_queue = []
    
    async def connect(self, websocket: WebSocket):
        """Connect a new WebSocket client."""
        await websocket.accept()
        self.active_connections.add(websocket)
        logger.info(f"✅ WebSocket connected. Active: {len(self.active_connections)}")
    
    async def disconnect(self, websocket: WebSocket):
        """Disconnect a WebSocket client."""
        self.active_connections.discard(websocket)
        logger.info(f"❌ WebSocket disconnected. Active: {len(self.active_connections)}")
    
    async def broadcast(self, message: dict):
        """Broadcast message to all connected clients."""
        if not self.active_connections:
            return
        
        disconnected = set()
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception as e:
                logger.error(f"Error sending message: {e}")
                disconnected.add(connection)
        
        # Remove disconnected clients
        for connection in disconnected:
            await self.disconnect(connection)
    
    async def send_to_client(self, websocket: WebSocket, message: dict):
        """Send message to specific client."""
        try:
            await websocket.send_json(message)
        except Exception as e:
            logger.error(f"Error sending to client: {e}")
            await self.disconnect(websocket)
    
    async def broadcast_market_data(self, symbol: str, data: dict):
        """Broadcast market data update."""
        message = {
            'type': 'market_data',
            'symbol': symbol,
            'data': data,
            'timestamp': datetime.utcnow().isoformat()
        }
        await self.broadcast(message)
    
    async def broadcast_trade(self, trade: dict):
        """Broadcast trade execution."""
        message = {
            'type': 'trade',
            'data': trade,
            'timestamp': datetime.utcnow().isoformat()
        }
        await self.broadcast(message)
    
    async def broadcast_alert(self, alert_type: str, message: str, severity: str = 'info'):
        """Broadcast alert notification."""
        alert = {
            'type': 'alert',
            'alert_type': alert_type,
            'message': message,
            'severity': severity,
            'timestamp': datetime.utcnow().isoformat()
        }
        await self.broadcast(alert)
