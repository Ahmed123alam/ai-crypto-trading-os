"""Agent 5: Smart Money & Whale Tracker."""
import logging
from typing import Dict, Optional

logger = logging.getLogger(__name__)


class WhaleTrackerAgent:
    """Smart Money & Whale Tracking Agent."""
    
    def __init__(self):
        self.name = "Whale Tracker"
        self.agent_type = "whale"
        self.performance = {
            'total_trades': 0,
            'win_rate': 0.5,
            'profit_factor': 1.0
        }
    
    async def analyze(self, market_data: Dict) -> Optional[Dict]:
        """Analyze whale movements for trading signals."""
        try:
            whale_data = market_data.get('whale_movements', {})
            if not whale_data:
                return None
            
            # Get whale activity
            large_buys = whale_data.get('large_buys', 0)
            large_sells = whale_data.get('large_sells', 0)
            exchange_inflows = whale_data.get('exchange_inflows', 0)  # volume
            exchange_outflows = whale_data.get('exchange_outflows', 0)  # volume
            liquidation_level = whale_data.get('liquidation_level', 0)
            current_price = market_data.get('current_price', 0)
            
            signal = None
            confidence = 0.0
            
            # Whale accumulation signal
            if exchange_outflows > exchange_inflows * 1.5 and large_buys > large_sells:
                signal = 'BUY'
                confidence = min(0.80, 0.5 + (exchange_outflows / (exchange_inflows + 1) - 1.5) * 0.2)
            
            # Whale distribution signal
            elif exchange_inflows > exchange_outflows * 1.5 and large_sells > large_buys:
                signal = 'SELL'
                confidence = min(0.80, 0.5 + (exchange_inflows / (exchange_outflows + 1) - 1.5) * 0.2)
            
            if signal:
                return {
                    'action': signal,
                    'confidence': confidence,
                    'agent': self.name,
                    'indicators': {
                        'large_buys': large_buys,
                        'large_sells': large_sells,
                        'exchange_inflows': exchange_inflows,
                        'exchange_outflows': exchange_outflows,
                        'liquidation_risk': abs(liquidation_level - current_price) / current_price if current_price > 0 else 0
                    },
                    'entry_reason': f"Whale {signal}: Outflow/Inflow ratio {exchange_outflows / (exchange_inflows + 1):.2f}x"
                }
        
        except Exception as e:
            logger.error(f"Whale Tracker analysis error: {e}")
        
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
