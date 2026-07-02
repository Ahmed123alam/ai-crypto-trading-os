# AI Trading Agents - Complete Guide

## Agent Framework Overview

All 5 agents operate independently but coordinate through a central **Consensus Engine** that validates and executes only high-conviction trades.

---

## Agent 1: High-Frequency Momentum Scalper

### Purpose
Captures explosive momentum during volatility spikes and order flow acceleration.

### Strategy Logic

```python
1. Monitor for momentum candlestick patterns
2. Detect volume expansion (2x+ average)
3. Check VWAP cross
4. Verify RSI acceleration
5. Enter immediately on confirmation
6. Exit on first signs of momentum decay
```

### Key Indicators
- **VWAP**: Volume-weighted average price
- **EMA 9/21**: Quick trend identification
- **MACD**: Momentum divergence
- **RSI**: Overbought acceleration
- **Delta Volume**: Order flow intensity

### Timeframes
- 1-minute (primary)
- 3-minute (confirmation)
- 5-minute (context)

### Entry Conditions
```
IF volume > 2 * average_volume
   AND RSI > 60
   AND MACD histogram expanding
   AND price above VWAP
THEN enter LONG
```

### Exit Conditions
```
IF profit_target_hit
   OR RSI starts declining
   OR volume drops below normal
   OR tight_stop_loss_hit
THEN close position
```

### Risk Parameters
- Max holding time: 5 minutes
- Stop loss: 0.5% below entry
- Take profit: 0.3-0.5%
- Position size: 1-2% of capital

---

## Agent 2: Market Maker & Order Flow AI

### Purpose
Analyzes Level 2 order book data to predict short-term price movements and liquidity shifts.

### Strategy Logic

```python
1. Analyze Level 2 order book depth
2. Calculate bid/ask imbalance
3. Detect hidden liquidity pools
4. Identify spoofed orders
5. Predict micro-structure movements
6. Execute before liquidity shift
```

### Key Metrics
- **Bid/Ask Ratio**: Order book imbalance
- **Order Book Depth**: Liquidity concentration
- **Heatmap**: Price level intensity
- **Footprint**: Volume at each level
- **Liquidation Pressure**: Forced selling

### Analysis Methods

**Heatmap Analysis:**
- Red zones: Resistance & liquidation levels
- Green zones: Support & buying pressure
- Volume intensity: Color saturation

**Order Flow Imbalance:**
```
IF (bid_volume / ask_volume) > 1.5
   AND price near support
THEN likely bounce
```

### Signals

1. **Liquidity Grab Detection**
   - Large orders suddenly appear
   - Price moves to fill them
   - Reversal follows

2. **Spoofing Detection**
   - Large orders appear
   - Disappear before fill
   - Price reverts

3. **Hidden Accumulation**
   - Iceberg orders detected
   - Consistent buying at level
   - Potential breakout

### Risk Parameters
- Max exposure: 5% at any price level
- Stop loss: Nearest level break
- Take profit: Next resistance
- Holding time: 1-15 minutes

---

## Agent 3: Mean Reversion Scalping AI

### Purpose
Captures quick snapback reversals when prices deviate significantly from fair value.

### Strategy Logic

```python
1. Calculate fair value (20-period EMA)
2. Measure deviation (Z-score)
3. Detect overbought/oversold (RSI/BB)
4. Wait for exhaustion signal
5. Enter on reversal confirmation
6. Exit near mean
```

### Key Indicators
- **Bollinger Bands**: Deviation measure
- **RSI**: Exhaustion detection
- **Z-Score**: Statistical deviation
- **ATR**: Volatility adjustment
- **Moving Average**: Fair value baseline

### Entry Signals

**Overbought Reversal:**
```
IF RSI > 70
   AND price > BB_upper + 2*ATR
   AND candle closes bearish
THEN enter SHORT
```

**Oversold Reversal:**
```
IF RSI < 30
   AND price < BB_lower - 2*ATR
   AND candle closes bullish
THEN enter LONG
```

### Exit Signals

```
IF price reaches MA (fair value)
   OR profit_target_hit
   OR time_exit (5 min)
THEN close
```

### Trade Mechanics
- Timeframes: 5m, 15m, 30m
- Holding time: 3-10 minutes
- Win rate target: 55-60%
- Risk/reward: 1:1.5 minimum

### Risk Parameters
- Position size: 2-3% per trade
- Stop loss: Beyond extremes
- Max daily trades: 20

---

## Agent 4: News & Sentiment Scalper

### Purpose
Trades market reactions to breaking news and sentiment shifts before mainstream adoption.

### Data Sources

1. **News Aggregators**
   - CoinDesk
   - CoinTelegraph
   - Bitcoin Magazine
   - Custom RSS feeds

2. **Social Sentiment**
   - Twitter/X trending
   - Reddit top posts
   - Telegram groups
   - Discord channels

3. **On-Chain Data**
   - Whale movements
   - Exchange flows
   - Liquidations
   - Smart contracts

### Sentiment Analysis Pipeline

```python
1. Collect news & social data
2. Parse and normalize text
3. Run NLP sentiment analysis
4. Calculate sentiment score (-1 to +1)
5. Compare to baseline
6. Generate trade signals
```

### Sentiment Scoring

```
+1.0 = Extremely bullish (strong buy)
+0.5 = Moderately bullish (buy)
 0.0 = Neutral
-0.5 = Moderately bearish (sell)
-1.0 = Extremely bearish (strong sell)
```

### Signal Generation

**Bullish Signals:**
- Regulatory approval news → LONG
- Partnership announcement → LONG
- Price target increase → LONG
- Major exchange listing → LONG

**Bearish Signals:**
- Regulatory ban → SHORT
- Security breach → SHORT
- Major hack → SHORT
- Liquidity concerns → SHORT

### Trading Logic

```python
IF sentiment_score > 0.7
   AND price below 50MA
   AND volume increasing
THEN enter LONG

IF sentiment_score < -0.7
   AND price above 50MA
   AND volume increasing
THEN enter SHORT
```

### Key Metrics
- Sentiment momentum (acceleration)
- Sentiment divergence (disagreement)
- Social volume spike
- News sentiment lag

### Risk Parameters
- Entry after news confirmation
- Tight stops around key levels
- Quick exits on reversal
- Position size: 2-4%

---

## Agent 5: Smart Money & Whale Tracker

### Purpose
Follows institutional and whale movements to anticipate market direction.

### Tracking Methods

1. **On-Chain Tracking**
   - Whale wallet addresses
   - Transfer amounts
   - Time of transfer
   - Destination addresses

2. **Exchange Monitoring**
   - Deposit/withdrawal flows
   - Exchange reserve changes
   - Outflow = potential bull
   - Inflow = potential bear

3. **Liquidation Maps**
   - Liquidation levels
   - Liquidation pressure
   - Cascade risk

### Data Providers

- **Whale Alert**: Large transactions
- **Glassnode**: On-chain metrics
- **Arkham**: Address clustering
- **CryptoQuant**: Exchange flows

### Key Signals

**Accumulation Signals:**
```
IF whale_address outflows from exchange
   AND amount > 1000 BTC equivalent
   AND price still low
THEN potential bull run
```

**Distribution Signals:**
```
IF whale_address deposits to exchange
   AND amount > 1000 BTC equivalent
   AND price near highs
THEN potential top
```

**Liquidation Cascade:**
```
IF liquidations > $100M at level
   AND price approaching level
THEN potential flash crash
```

### Trading Strategy

```python
1. Identify smart money address patterns
2. Monitor their recent moves
3. Follow their new positions
4. Enter 5-30 minutes after their move
5. Use their exit as stop loss
```

### Risk Parameters
- Follow 2-5 trusted whale addresses
- Position size: 3-5%
- Hold duration: 15min - 2hours
- Stop: Beyond whale entry

---

## Central AI Consensus Engine

### Purpose
Aggregates signals from all 5 agents and executes only high-conviction trades.

### Consensus Algorithm

```python
# Collect signals from all agents
signals = {
    'momentum': agent1.signal,      # Buy/Sell/Neutral
    'orderflow': agent2.signal,
    'meanreversion': agent3.signal,
    'sentiment': agent4.signal,
    'whale': agent5.signal
}

# Calculate confidence score (0-100)
confidence = calculate_consensus(signals)

# Risk check
risk_score = risk_management.evaluate()

# Execute if conditions met
if confidence > 70 and risk_score < 5:
    execute_trade(signals, confidence)
else:
    skip_trade()
```

### Consensus Modes

**Conservative (Confidence > 80)**
- Requires 4-5 agents agreement
- Tight stops
- Small position size
- Best for trending markets

**Balanced (Confidence > 70)**
- Requires 3+ agents agreement
- Medium stops
- Medium position size
- Default mode

**Aggressive (Confidence > 60)**
- Requires 2+ agents agreement
- Wider stops
- Larger position size
- Volatile markets only

### Trade Approval Process

1. **Signal Collection** (100ms)
   - Gather signals from all agents
   - Timestamp each signal

2. **Signal Validation** (50ms)
   - Check signal consistency
   - Verify market conditions
   - Check technical levels

3. **Risk Assessment** (100ms)
   - Check position size
   - Check daily drawdown
   - Check correlation risk
   - Check leverage levels

4. **Execution** (50ms)
   - Create order
   - Submit to exchange
   - Log trade
   - Notify dashboard

### Conflict Resolution

**If agents disagree:**
- Skip trade
- Wait for consensus
- Use tie-breaker metrics
- Log disagreement

---

## Agent Coordination

### Communication Protocol

```
Redis Pub/Sub
    ├─ Agent signals
    ├─ Risk alerts
    ├─ Trade execution
    └─ Performance metrics
```

### Performance Metrics

Each agent tracks:
- Win rate (target: >50%)
- Profit factor (target: >1.5)
- Sharpe ratio (target: >1.0)
- Max drawdown (limit: 20%)
- Trade frequency
- Average holding time

### Agent Health Monitoring

```python
if agent_performance.win_rate < 0.45:
    agent.disable()  # Pause agent
    alert_team()     # Notify operators

if agent_performance.drawdown > 0.30:
    agent.reduce_position_size()
    agent.tighten_stops()
```

---

## Continuous Improvement

### Learning System

1. **Daily Review**
   - Winning vs losing trades
   - Agent performance
   - Market regime changes

2. **Weekly Optimization**
   - Parameter tuning
   - Threshold adjustment
   - Signal weighting

3. **Monthly Retraining**
   - New market data
   - New patterns
   - ML model updates

### Feedback Loop

```
Trade Execution
    ↓
Performance Tracking
    ↓
Metric Analysis
    ↓
Parameter Adjustment
    ↓
Retraining
    ↓
Back to Trading
```
