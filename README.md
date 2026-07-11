# 🐂 Bull Market Engine

## AI-Powered Quantitative Trading & Portfolio Intelligence System

The **Bull Market Engine** is a quantitative investment research platform designed to identify high-potential stocks using technical analysis, market intelligence, risk management, portfolio optimization, and algorithmic trading techniques.

The system combines multiple market factors into a unified scoring framework:

* Trend strength
* Momentum
* Institutional volume activity
* Volatility and risk
* Relative market performance
* Market breadth
* Portfolio optimization

The goal is to transform raw market data into:

```
Market Data
      |
      ↓
Feature Engineering
      |
      ↓
Technical Intelligence
      |
      ↓
Bull Market Score
      |
      ↓
Trading Signals
      |
      ↓
Portfolio Optimization
      |
      ↓
Backtesting
      |
      ↓
Dashboard
```

---

# 🚀 Features

## Current Implementation

### Market Data Engine

* Yahoo Finance integration
* Historical OHLCV data
* Multi-stock download
* Benchmark comparison

Supported:

* Stocks
* ETFs
* Indices

---

# Technical Intelligence Layer

The engine calculates multiple quantitative factors.

## 1. Trend Engine

File:

```
indicators/trend.py
```

Features:

* Moving averages
* EMA crossover
* SMA trend
* ADX
* Trend strength score

Output:

```
Trend_Score: 0-100
```

---

## 2. Momentum Engine

File:

```
indicators/momentum.py
```

Indicators:

* RSI
* MACD
* ROC
* Stochastic Oscillator
* Williams %R

Output:

```
Momentum_Score: 0-100
```

---

## 3. Volume Intelligence Engine

File:

```
indicators/volume.py
```

Indicators:

* Volume moving average
* Volume ratio
* Volume spike detection
* OBV
* Chaikin Money Flow
* Money Flow Index
* Accumulation/Distribution

Purpose:

Detect institutional accumulation.

Output:

```
Volume_Score: 0-100
```

---

## 4. Volatility & Risk Engine

File:

```
indicators/volatility.py
```

Indicators:

* ATR
* Bollinger Bands
* Historical volatility
* Volatility regime detection

Output:

```
Risk_Score: 0-100
```

---

## 5. Relative Strength Engine

File:

```
indicators/strength.py
```

Measures:

* Stock performance vs benchmark
* Alpha
* Beta
* Sharpe Ratio
* Information Ratio

Output:

```
Strength_Score: 0-100
```

---

## 6. Market Breadth Engine

File:

```
indicators/breadth.py
```

Measures:

* Advance/Decline ratio
* Stocks above 200 SMA
* New highs/new lows
* Market participation

Output:

```
Breadth_Score: 0-100
```

---

# 🧠 Bull Market Scoring System

File:

```
strategy/scoring.py
```

The engine combines all factors:

```
Bull Market Score =
```

```
25% Trend
+
20% Momentum
+
15% Volume
+
15% Relative Strength
+
10% Risk
+
10% Quality
+
5% Market Breadth
```

Final output:

Example:

| Stock | Score | Signal     |
| ----- | ----- | ---------- |
| NVDA  | 94    | STRONG BUY |
| AMD   | 86    | BUY        |
| MSFT  | 82    | BUY        |
| TSLA  | 58    | HOLD       |

---

# 📈 Trading Signal Engine

File:

```
strategy/signals.py
```

Creates:

## Entry Signals

Conditions:

* Strong Bull Market Score
* Positive trend
* Positive momentum
* Acceptable risk

Example:

```
BUY
```

---

## Exit Signals

Conditions:

* Score deterioration
* Trend breakdown
* Momentum weakness

Example:

```
SELL
```

---

## Risk Management

The engine calculates:

* Stop loss
* Take profit
* Risk/reward ratio
* Position size
* Trailing stops

Example:

```
Entry Price:     $145

Stop Loss:       $137

Target:          $175

Risk Reward:     3.7

Position Size:   68 shares
```

---

# 📂 Project Structure

```
bull_market_engine/

│
├── README.md
├── requirements.txt
├── config.py
├── main.py
│
│
├── data/
│   │
│   ├── yahoo.py
│   ├── loader.py
│   └── cache.py
│
│
├── indicators/
│   │
│   ├── trend.py
│   ├── momentum.py
│   ├── volume.py
│   ├── volatility.py
│   ├── strength.py
│   └── breadth.py
│
│
├── strategy/
│   │
│   ├── scoring.py
│   └── signals.py
│
│
├── portfolio/
│   │
│   ├── optimizer.py
│   ├── risk.py
│   └── allocation.py
│
│
├── backtest/
│   │
│   ├── engine.py
│   ├── metrics.py
│   └── reports.py
│
│
├── dashboard/
│   │
│   ├── app.py
│   ├── charts.py
│   └── components.py
│
│
├── models/
│   │
│   └── saved_models/
│
│
└── notebooks/
    │
    ├── exploration.ipynb
    └── research.ipynb

```

---

# Installation

## 1. Clone Repository

```bash
git clone https://github.com/username/bull-market-engine.git

cd bull-market-engine
```

---

## 2. Create Environment

Using Conda:

```bash
conda create \
-n bull_engine \
python=3.11
```

Activate:

```bash
conda activate bull_engine
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Requirements

Main libraries:

```
pandas
numpy

yfinance

ta

scikit-learn

scipy

cvxpy

plotly

streamlit

matplotlib

seaborn
```

---

# Configuration

File:

```
config.py
```

Example:

```python
INITIAL_CAPITAL = 100000

STOP_LOSS = 0.08

TAKE_PROFIT = 0.20


FACTOR_WEIGHTS = {

    "trend":0.25,

    "momentum":0.20,

    "volume":0.15,

    "relative_strength":0.15,

    "volatility":0.10,

    "quality":0.10,

    "breadth":0.05
}

```

---

# Data Pipeline

Example:

```python
from data.yahoo import download_symbol


data = download_symbol(

    "AMD",

    period="5y"

)
```

Returns:

```
Date

Open

High

Low

Close

Volume
```

---

# Running the Analysis

Example:

```python
from strategy.scoring import run_scoring_engine


result = run_scoring_engine(data)


print(

result[
[
"Bull_Market_Score",
"Signal"
]

]

)
```

Output:

```
Bull_Market_Score     Signal

92                   STRONG BUY
```

---

# Portfolio Optimization Engine

Upcoming module:

```
portfolio/
```

Planned features:

## Mean Variance Optimization

* Efficient frontier
* Maximum Sharpe portfolio
* Minimum volatility portfolio

## Risk Parity

Balances:

* Volatility contribution
* Asset risk

## Black-Litterman Model

Combines:

* Market equilibrium
* Investor views

Output:

Example:

```
Portfolio Allocation

AMD       18%
NVDA      25%
MSFT      20%
GOOG      15%
Cash      22%
```

---

# Backtesting Engine

Upcoming:

```
backtest/
```

Features:

* Historical simulation
* Walk-forward testing
* Transaction costs
* Slippage
* Benchmark comparison

Metrics:

* CAGR
* Sharpe Ratio
* Maximum Drawdown
* Win Rate
* Profit Factor

Example:

```
Strategy Performance

Return:          32%

CAGR:            18%

Sharpe:          1.85

Max Drawdown:    -12%

Win Rate:        64%
```

---

# Dashboard

Upcoming:

```
dashboard/
```

Built with:

* Streamlit
* Plotly

Dashboard sections:

## Market Scanner

Displays:

* Top ranked stocks
* Bull Market Score
* Trading signal

## Stock Analysis

Charts:

* Price action
* Indicators
* Momentum
* Volume

## Portfolio View

Displays:

* Allocation
* Risk
* Performance

## Backtesting

Displays:

* Equity curve
* Drawdown
* Returns

---

# Future AI Extensions

Planned:

## Machine Learning Ranking Model

Models:

* XGBoost
* LightGBM
* Random Forest
* Neural Networks

Features:

* Technical indicators
* Earnings data
* Sentiment
* Macro factors

---

## Alternative Data

Future integration:

* News sentiment
* SEC filings
* Options flow
* Insider transactions
* Institutional holdings

---

# Development Roadmap

## Phase 1 — Core Engine

Completed:

✅ Data ingestion
✅ Indicators
✅ Scoring system
✅ Trading signals

---

## Phase 2 — Portfolio Intelligence

Next:

⬜ Portfolio optimizer
⬜ Risk model
⬜ Allocation engine

---

## Phase 3 — Backtesting

Next:

⬜ Simulation engine
⬜ Performance metrics
⬜ Strategy evaluation

---

## Phase 4 — Dashboard

Next:

⬜ Streamlit UI
⬜ Interactive charts
⬜ Portfolio monitoring

---

# Disclaimer

This project is for:

* Quantitative research
* Education
* Algorithm development

It is not financial advice.

Always validate strategies using historical testing and proper risk management before applying them to real capital.

---

# Author

Bull Market Engine

AI + Quantitative Finance Research Project
