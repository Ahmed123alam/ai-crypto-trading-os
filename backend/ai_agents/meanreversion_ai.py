"""Agent 3: Mean Reversion Scalping AI."""
import logging
from typing import Dict, Optional
import numpy as np
from talib import EMA, RSI, BBANDS

logger = logging.getLogger(__name__)


class MeanReversionAgent:
    """Mean Reversion Scalping Agent."""
    
    def __init__(self):
        self.name = "Mean Reversion AI"
        self.agent_type = "meanreversion"
        self.performance = {
            'total_trades': 0,
            'win_rate': 0.5,
            'profit_factor': 1.0
        }
    
    async def analyze(self, market_data: Dict) -> Optional[Dict]:
        """Analyze for mean reversion opportunities."""
        try:
            candles = market_data.get('candles', [])
            if len(candles) < 30:
                return None
            
            closes = np.array([c['close'] for c in candles])
            
            # Calculate indicators
            rsi = RSI(closes, timeperiod=14)
            ema20 = EMA(closes, timeperiod=20)
            upper, middle, lower = BBANDS(closes, timeperiod=20, nbdevup=2, nbdevdn=2)
            
            # Current values
            current_close = closes[-1]
            current_rsi = rsi[-1]
            current_ema20 = ema20[-1]
            current_upper = upper[-1]
            current_lower = lower[-1]
            current_middle = middle[-1]
            
            signal = None
            confidence = 0.0
            
            # Oversold reversion
            if (
                current_rsi < 30 and
                current_close < current_lower and
                closes[-1] > closes[-2]  # Reversal candle
            ):
                signal = 'BUY'
                confidence = min(0.80, 0.5 + (30 - current_rsi) / 30 * 0.3)
            
            # Overbought reversion
            elif (
                current_rsi > 70 and
                current_close > current_upper and
                closes[-1] < closes[-2]  # Reversal candle
            ):
                signal = 'SELL'
                confidence = min(0.80, 0.5 + (current_rsi - 70) / 30 * 0.3)
            
            if signal:
                return {
                    'action': signal,
                    'confidence': confidence,
                    'agent': self.name,
                    'indicators': {
                        'rsi': current_rsi,
                        'price_position': 'above_upper' if current_close > current_upper else 'below_lower',
                        'distance_to_mean': abs(current_close - current_middle) / current_middle
                    },
                    'entry_reason': f"Mean Reversion {signal}: RSI {current_rsi:.1f}"
                }
        
        except Exception as e:
            logger.error(f"Mean Reversion AI analysis error: {e}")
        
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
