"""
config.py

Global configuration for Bull Market Engine
"""

from pathlib import Path

# =============================================================================
# PROJECT PATHS
# =============================================================================

BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = BASE_DIR / "data"
CACHE_DIR = BASE_DIR / "cache"
LOG_DIR = BASE_DIR / "logs"
REPORT_DIR = BASE_DIR / "reports"

for directory in [DATA_DIR, CACHE_DIR, LOG_DIR, REPORT_DIR]:
    directory.mkdir(exist_ok=True)

# =============================================================================
# MARKET SETTINGS
# =============================================================================

DEFAULT_EXCHANGE = "NSE"

DEFAULT_BENCHMARK = "^NSEI"

DEFAULT_INTERVAL = "1d"

DEFAULT_PERIOD = "5y"

SUPPORTED_INTERVALS = [
    "1m",
    "2m",
    "5m",
    "15m",
    "30m",
    "60m",
    "90m",
    "1d",
    "1wk",
    "1mo"
]

# =============================================================================
# RISK SETTINGS
# =============================================================================

RISK_FREE_RATE = 0.07          # 7%

MAX_PORTFOLIO_SIZE = 20

DEFAULT_POSITION_SIZE = 0.05   # 5%

MAX_SINGLE_POSITION = 0.10      # 10%

STOP_LOSS = 0.08               # 8%

TAKE_PROFIT = 0.20             # 20%

TRAILING_STOP = True

# =============================================================================
# TECHNICAL INDICATORS
# =============================================================================

EMA_FAST = 20
EMA_SLOW = 50

LONG_TREND = 200

RSI_PERIOD = 14

MACD_FAST = 12
MACD_SLOW = 26
MACD_SIGNAL = 9

ATR_PERIOD = 14

ADX_PERIOD = 14

BOLLINGER_PERIOD = 20
BOLLINGER_STD = 2

SUPERTREND_PERIOD = 10
SUPERTREND_MULTIPLIER = 3

# =============================================================================
# BACKTEST SETTINGS
# =============================================================================

INITIAL_CAPITAL = 1_000_000

COMMISSION = 0.001

SLIPPAGE = 0.0005

REBALANCE_FREQUENCY = "M"

# =============================================================================
# PORTFOLIO OPTIMIZATION
# =============================================================================

EXPECTED_RETURN_METHOD = "mean_historical"

RISK_MODEL = "sample_cov"

OPTIMIZER = "max_sharpe"

# Other options:
# min_volatility
# efficient_risk
# efficient_return
# equal_weight
# risk_parity

# =============================================================================
# FACTOR WEIGHTS
# =============================================================================

FACTOR_WEIGHTS = {

    "trend": 0.25,

    "momentum": 0.20,

    "volume": 0.15,

    "relative_strength": 0.15,

    "volatility": 0.10,

    "quality": 0.10,

    "breadth": 0.05
}

# =============================================================================
# DASHBOARD
# =============================================================================

APP_NAME = "Bull Market Engine"

APP_THEME = "dark"

REFRESH_SECONDS = 300

# =============================================================================
# LOGGING
# =============================================================================

LOG_LEVEL = "INFO"

LOG_FILE = LOG_DIR / "bull_engine.log"

# =============================================================================
# CACHE
# =============================================================================

CACHE_ENABLED = True

CACHE_EXPIRY_HOURS = 12

# =============================================================================
# WATCHLIST
# =============================================================================

DEFAULT_WATCHLIST = [

    "RELIANCE.NS",

    "TCS.NS",

    "HDFCBANK.NS",

    "INFY.NS",

    "ICICIBANK.NS",

    "SBIN.NS",

    "ITC.NS",

    "LT.NS",

    "BHARTIARTL.NS",

    "HINDUNILVR.NS"

]

# =============================================================================
# EXPORTS
# =============================================================================

__all__ = [
    "BASE_DIR",
    "DATA_DIR",
    "CACHE_DIR",
    "REPORT_DIR",
    "DEFAULT_BENCHMARK",
    "DEFAULT_PERIOD",
    "DEFAULT_INTERVAL",
    "FACTOR_WEIGHTS",
]