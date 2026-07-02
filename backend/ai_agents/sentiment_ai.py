"""Agent 4: News & Sentiment Scalper."""
import logging
from typing import Dict, Optional
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class SentimentAgent:
    """News & Sentiment Analysis Agent."""
    
    def __init__(self):
        self.name = "Sentiment AI"
        self.agent_type = "sentiment"
        self.performance = {
            'total_trades': 0,
            'win_rate': 0.5,
            'profit_factor': 1.0
        }
    
    async def analyze(self, market_data: Dict) -> Optional[Dict]:
        """Analyze sentiment for trading signals."""
        try:
            sentiment_data = market_data.get('sentiment', {})
            if not sentiment_data:
                return None
            
            # Get sentiment scores
            news_sentiment = sentiment_data.get('news_sentiment', 0)  # -1 to 1
            social_sentiment = sentiment_data.get('social_sentiment', 0)  # -1 to 1
            volume_spike = sentiment_data.get('social_volume_spike', 0)  # 0 to 1
            recent_news = sentiment_data.get('recent_news', [])
            
            # Calculate composite sentiment
            composite_sentiment = (news_sentiment * 0.4 + social_sentiment * 0.6)
            
            signal = None
            confidence = 0.0
            
            # Strong bullish sentiment
            if composite_sentiment > 0.7 and volume_spike > 0.5:
                signal = 'BUY'
                confidence = min(0.85, abs(composite_sentiment))
            
            # Strong bearish sentiment
            elif composite_sentiment < -0.7 and volume_spike > 0.5:
                signal = 'SELL'
                confidence = min(0.85, abs(composite_sentiment))
            
            if signal:
                recent_headlines = [n.get('headline', '') for n in recent_news[:3]]
                return {
                    'action': signal,
                    'confidence': confidence,
                    'agent': self.name,
                    'indicators': {
                        'news_sentiment': news_sentiment,
                        'social_sentiment': social_sentiment,
                        'composite_sentiment': composite_sentiment,
                        'volume_spike': volume_spike
                    },
                    'entry_reason': f"Sentiment {signal}: Score {composite_sentiment:.2f}",
                    'news_context': recent_headlines
                }
        
        except Exception as e:
            logger.error(f"Sentiment AI analysis error: {e}")
        
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
