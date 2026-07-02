"""Database models."""
from sqlalchemy import Column, String, Float, Integer, DateTime, Boolean, JSON, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.database import Base


class User(Base):
    """User model."""
    __tablename__ = "users"
    
    id = Column(String, primary_key=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    portfolios = relationship("Portfolio", back_populates="user")
    trades = relationship("Trade", back_populates="user")


class Portfolio(Base):
    """Portfolio model."""
    __tablename__ = "portfolios"
    
    id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey("users.id"))
    name = Column(String)
    total_balance = Column(Float, default=0.0)
    available_balance = Column(Float, default=0.0)
    unrealized_pnl = Column(Float, default=0.0)
    realized_pnl = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = relationship("User", back_populates="portfolios")
    positions = relationship("Position", back_populates="portfolio")
    trades = relationship("Trade", back_populates="portfolio")


class Position(Base):
    """Open position model."""
    __tablename__ = "positions"
    
    id = Column(String, primary_key=True)
    portfolio_id = Column(String, ForeignKey("portfolios.id"))
    symbol = Column(String, index=True)
    side = Column(String)  # LONG or SHORT
    quantity = Column(Float)
    entry_price = Column(Float)
    current_price = Column(Float)
    unrealized_pnl = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    portfolio = relationship("Portfolio", back_populates="positions")


class Trade(Base):
    """Trade history model."""
    __tablename__ = "trades"
    
    id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey("users.id"))
    portfolio_id = Column(String, ForeignKey("portfolios.id"))
    symbol = Column(String, index=True)
    side = Column(String)  # BUY or SELL
    quantity = Column(Float)
    entry_price = Column(Float)
    exit_price = Column(Float, nullable=True)
    pnl = Column(Float, default=0.0)
    pnl_percent = Column(Float, default=0.0)
    status = Column(String)  # OPEN, CLOSED, CANCELLED
    agent_name = Column(String, nullable=True)
    confidence = Column(Float, default=0.0)
    reason = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    closed_at = Column(DateTime, nullable=True)
    
    user = relationship("User", back_populates="trades")
    portfolio = relationship("Portfolio", back_populates="trades")


class Strategy(Base):
    """Trading strategy model."""
    __tablename__ = "strategies"
    
    id = Column(String, primary_key=True)
    name = Column(String, unique=True, index=True)
    description = Column(String)
    agent_type = Column(String)  # momentum, orderflow, meanreversion, sentiment, whale
    parameters = Column(JSON)
    is_active = Column(Boolean, default=False)
    win_rate = Column(Float, default=0.0)
    profit_factor = Column(Float, default=0.0)
    total_trades = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Alert(Base):
    """Trading alert model."""
    __tablename__ = "alerts"
    
    id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey("users.id"))
    alert_type = Column(String)  # trade, risk, opportunity
    message = Column(String)
    severity = Column(String)  # info, warning, critical
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
