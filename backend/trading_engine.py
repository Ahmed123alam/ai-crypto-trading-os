"""Trading Engine - CCXT Integration."""
import logging
import asyncio
from typing import Dict, List, Optional
import ccxt
from ccxt.base.errors import ExchangeError, NetworkError

logger = logging.getLogger(__name__)


class TradingEngine:
    """Unified trading engine with multi-exchange support via CCXT."""
    
    def __init__(self, config: Dict):
        self.config = config
        self.exchanges: Dict = {}
        self.is_running = False
        self._initialize_exchanges()
    
    def _initialize_exchanges(self):
        """Initialize all configured exchanges."""
        # Binance
        if self.config.get('BINANCE_API_KEY'):
            self.exchanges['binance'] = ccxt.binance({
                'apiKey': self.config['BINANCE_API_KEY'],
                'secret': self.config['BINANCE_API_SECRET'],
                'enableRateLimit': True,
            })
            logger.info("✅ Binance initialized")
        
        # Bybit
        if self.config.get('BYBIT_API_KEY'):
            self.exchanges['bybit'] = ccxt.bybit({
                'apiKey': self.config['BYBIT_API_KEY'],
                'secret': self.config['BYBIT_API_SECRET'],
                'enableRateLimit': True,
            })
            logger.info("✅ Bybit initialized")
        
        # OKX
        if self.config.get('OKX_API_KEY'):
            self.exchanges['okx'] = ccxt.okx({
                'apiKey': self.config['OKX_API_KEY'],
                'secret': self.config['OKX_API_SECRET'],
                'password': self.config.get('OKX_PASSPHRASE', ''),
                'enableRateLimit': True,
            })
            logger.info("✅ OKX initialized")
    
    async def get_ticker(self, symbol: str, exchange: str = 'binance') -> Dict:
        """Get ticker information."""
        try:
            if exchange not in self.exchanges:
                raise ValueError(f"Exchange {exchange} not initialized")
            
            ticker = await self.exchanges[exchange].fetch_ticker(symbol)
            return ticker
        except ExchangeError as e:
            logger.error(f"Exchange error: {e}")
            raise
        except NetworkError as e:
            logger.error(f"Network error: {e}")
            raise
    
    async def get_order_book(self, symbol: str, limit: int = 50, exchange: str = 'binance') -> Dict:
        """Get order book data."""
        try:
            if exchange not in self.exchanges:
                raise ValueError(f"Exchange {exchange} not initialized")
            
            order_book = await self.exchanges[exchange].fetch_order_book(symbol, limit=limit)
            return order_book
        except Exception as e:
            logger.error(f"Order book fetch error: {e}")
            raise
    
    async def create_order(
        self,
        symbol: str,
        order_type: str,
        side: str,
        amount: float,
        price: Optional[float] = None,
        exchange: str = 'binance'
    ) -> Dict:
        """Create a trading order."""
        try:
            if exchange not in self.exchanges:
                raise ValueError(f"Exchange {exchange} not initialized")
            
            if order_type == 'market':
                order = await self.exchanges[exchange].create_market_order(
                    symbol, side, amount
                )
            elif order_type == 'limit':
                if price is None:
                    raise ValueError("Price required for limit orders")
                order = await self.exchanges[exchange].create_limit_order(
                    symbol, side, amount, price
                )
            else:
                raise ValueError(f"Unknown order type: {order_type}")
            
            logger.info(f"🚧 Order created: {side} {amount} {symbol} @ {price}")
            return order
        except Exception as e:
            logger.error(f"Order creation error: {e}")
            raise
    
    async def get_open_orders(self, symbol: Optional[str] = None, exchange: str = 'binance') -> List[Dict]:
        """Get open orders."""
        try:
            if exchange not in self.exchanges:
                raise ValueError(f"Exchange {exchange} not initialized")
            
            orders = await self.exchanges[exchange].fetch_open_orders(symbol)
            return orders
        except Exception as e:
            logger.error(f"Fetch open orders error: {e}")
            raise
    
    async def get_balance(self, exchange: str = 'binance') -> Dict:
        """Get account balance."""
        try:
            if exchange not in self.exchanges:
                raise ValueError(f"Exchange {exchange} not initialized")
            
            balance = await self.exchanges[exchange].fetch_balance()
            return balance
        except Exception as e:
            logger.error(f"Balance fetch error: {e}")
            raise
    
    async def shutdown(self):
        """Shutdown trading engine."""
        self.is_running = False
        for exchange in self.exchanges.values():
            await exchange.close()
        logger.info("🛑 Trading Engine shutdown")


async def init_trading_engine():
    """Initialize trading engine."""
    from backend.config import settings
    
    config = {
        'BINANCE_API_KEY': settings.BINANCE_API_KEY,
        'BINANCE_API_SECRET': settings.BINANCE_API_SECRET,
        'BYBIT_API_KEY': settings.BYBIT_API_KEY,
        'BYBIT_API_SECRET': settings.BYBIT_API_SECRET,
        'OKX_API_KEY': settings.OKX_API_KEY,
        'OKX_API_SECRET': settings.OKX_API_SECRET,
        'OKX_PASSPHRASE': settings.OKX_API_KEY,  # placeholder
    }
    
    engine = TradingEngine(config)
    logger.info("🚀 Trading Engine initialized")
    return engine
