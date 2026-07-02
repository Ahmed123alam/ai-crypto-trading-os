"""Agent 1: High-Frequency Momentum Scalper."""
import logging
from typing import Dict, Optional
import numpy as np
from talib import EMA, MACD, RSI

logger = logging.getLogger(__name__)


class MomentumScalperAgent:
    """High-Frequency Momentum Scalping Agent."""
    
    def __init__(self):
        self.name = "Momentum Scalper"
        self.agent_type = "momentum"
        self.performance = {
            'total_trades': 0,
            'win_rate': 0.5,
            'profit_factor': 1.0
        }
    
    async def analyze(self, market_data: Dict) -> Optional[Dict]:
        """Analyze market for momentum opportunities."""
        try:
            candles = market_data.get('candles', [])
            if len(candles) < 30:
                return None
            
            closes = np.array([c['close'] for c in candles])
            volumes = np.array([c['volume'] for c in candles])
            highs = np.array([c['high'] for c in candles])
            lows = np.array([c['low'] for c in candles])
            
            # Calculate indicators
            ema9 = EMA(closes, timeperiod=9)
            ema21 = EMA(closes, timeperiod=21)
            macd, signal, hist = MACD(closes, fastperiod=12, slowperiod=26, signalperiod=9)
            rsi = RSI(closes, timeperiod=14)
            
            # Current values
            current_close = closes[-1]
            current_volume = volumes[-1]
            avg_volume = np.mean(volumes[-20:])
            current_rsi = rsi[-1]
            current_macd_hist = hist[-1]
            current_ema9 = ema9[-1]
            current_ema21 = ema21[-1]
            
            # Signal logic
            signal = None
            confidence = 0.0
            
            # Bullish momentum conditions
            if (
                current_volume > 2 * avg_volume and
                current_rsi > 60 and
                current_macd_hist > 0 and
                current_close > current_ema9 > current_ema21
            ):
                signal = 'BUY'
                confidence = min(0.9, 0.5 + (current_volume / avg_volume - 2) * 0.2 + (current_rsi - 60) / 40 * 0.2)
            
            # Bearish momentum conditions
            elif (
                current_volume > 2 * avg_volume and
                current_rsi < 40 and
                current_macd_hist < 0 and
                current_close < current_ema9 < current_ema21
            ):
                signal = 'SELL'
                confidence = min(0.9, 0.5 + (current_volume / avg_volume - 2) * 0.2 + (40 - current_rsi) / 40 * 0.2)
            
            if signal:
                return {
                    'action': signal,
                    'confidence': confidence,
                    'agent': self.name,
                    'indicators': {
                        'volume_ratio': current_volume / avg_volume,
                        'rsi': current_rsi,
                        'macd_histogram': current_macd_hist,
                        'price_position': 'above_ema' if current_close > current_ema21 else 'below_ema'
                    },
                    'entry_reason': f"Momentum {signal}: Volume {current_volume/avg_volume:.1f}x, RSI {current_rsi:.1f}"
                }
        
        except Exception as e:
            logger.error(f"Momentum Scalper analysis error: {e}")
        
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
