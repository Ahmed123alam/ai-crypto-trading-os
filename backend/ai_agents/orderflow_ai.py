"""Agent 2: Market Maker & Order Flow AI."""
import logging
from typing import Dict, Optional
import numpy as np

logger = logging.getLogger(__name__)


class OrderFlowAgent:
    """Market Maker & Order Flow Analysis Agent."""
    
    def __init__(self):
        self.name = "Order Flow AI"
        self.agent_type = "orderflow"
        self.performance = {
            'total_trades': 0,
            'win_rate': 0.5,
            'profit_factor': 1.0
        }
    
    async def analyze(self, market_data: Dict) -> Optional[Dict]:
        """Analyze order flow for trading signals."""
        try:
            order_book = market_data.get('order_book', {})
            if not order_book:
                return None
            
            bids = order_book.get('bids', [])
            asks = order_book.get('asks', [])
            
            if not bids or not asks:
                return None
            
            # Calculate order book imbalance
            bid_volume = sum(float(b[1]) for b in bids[:10])  # Top 10 bids
            ask_volume = sum(float(a[1]) for a in asks[:10])  # Top 10 asks
            
            imbalance_ratio = bid_volume / ask_volume if ask_volume > 0 else 0
            
            # Get price levels
            best_bid = float(bids[0][0])
            best_ask = float(asks[0][0])
            mid_price = (best_bid + best_ask) / 2
            spread = best_ask - best_bid
            
            # Analyze liquidity pressure
            signal = None
            confidence = 0.0
            
            # Strong buy pressure
            if imbalance_ratio > 1.5:
                signal = 'BUY'
                confidence = min(0.85, 0.5 + (imbalance_ratio - 1.5) * 0.2)
            
            # Strong sell pressure
            elif imbalance_ratio < 0.67:
                signal = 'SELL'
                confidence = min(0.85, 0.5 + (1 - imbalance_ratio) * 0.2)
            
            if signal:
                return {
                    'action': signal,
                    'confidence': confidence,
                    'agent': self.name,
                    'indicators': {
                        'bid_ask_imbalance': imbalance_ratio,
                        'bid_volume': bid_volume,
                        'ask_volume': ask_volume,
                        'spread': spread,
                        'mid_price': mid_price
                    },
                    'entry_reason': f"Order Flow {signal}: Imbalance {imbalance_ratio:.2f}x"
                }
        
        except Exception as e:
            logger.error(f"Order Flow AI analysis error: {e}")
        
        return None
    
    async def get_health(self) -> Dict:
        """Get agent health status."""
        is_healthy = self.performance['win_rate'] > 0.45
        return {
            'status': 'healthy' if is_healthy else 'unhealthy',
            'performance': self.performance
        }
    
    async def recover(self):
        """Recover from unhealthy state."""
        logger.info(f"🔧 Recovering {self.name}...")
        self.performance['total_trades'] = 0
        self.performance['win_rate'] = 0.5
        self.performance['profit_factor'] = 1.0
