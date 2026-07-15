"""
loader.py

Unified market data loader.

Responsible for:
- Loading multiple assets
- Cleaning datasets
- Creating price matrix
- Creating returns matrix
- Preparing portfolio data
"""
import sys
from pathlib import Path
# Allow importing config when running script directly
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from typing import List, Dict

import pandas as pd


from config import (
    DEFAULT_PERIOD,
    DEFAULT_INTERVAL
)


from data.yahoo import (
    download_symbol
)



# =============================================================================
# LOAD SINGLE ASSET
# =============================================================================


def load_asset(
        symbol: str,
        period: str = DEFAULT_PERIOD,
        interval: str = DEFAULT_INTERVAL
):
    """
    Load one stock.

    Returns
    -------
    DataFrame
    """


    df = download_symbol(
        symbol=symbol,
        period=period,
        interval=interval
    )


    return df



# =============================================================================
# LOAD MULTIPLE ASSETS
# =============================================================================


def load_market_data(
        symbols: List[str],
        period: str = DEFAULT_PERIOD,
        interval: str = DEFAULT_INTERVAL
):
    """
    Download multiple assets.

    Returns
    -------
    Dictionary

    Example:

    {
        "TCS.NS": dataframe,
        "INFY.NS": dataframe
    }

    """


    market_data = {}


    for symbol in symbols:

        print(
            f"Loading {symbol}"
        )


        market_data[symbol] = load_asset(
            symbol,
            period,
            interval
        )


    return market_data




# =============================================================================
# CREATE PRICE MATRIX
# =============================================================================


def price_matrix(
        market_data: Dict[str, pd.DataFrame]
):
    """
    Convert OHLCV data into price matrix.

    Used by:
    - Portfolio optimizer
    - Correlation analysis

    Output:

    Date          TCS       INFY
    2025-01-01   4100      1800

    """


    prices = {}


    for symbol, df in market_data.items():

        prices[symbol] = (
            df["Adj Close"]
        )


    return pd.DataFrame(prices)




# =============================================================================
# CREATE RETURNS MATRIX
# =============================================================================


def returns_matrix(
        market_data: Dict[str, pd.DataFrame]
):
    """
    Create daily returns matrix.
    """


    prices = price_matrix(
        market_data
    )


    returns = (
        prices
        .pct_change()
        .dropna()
    )


    return returns




# =============================================================================
# ALIGN DATASETS
# =============================================================================


def align_market_data(
        market_data
):
    """
    Synchronize dates between assets.

    Removes missing trading days.
    """


    prices = price_matrix(
        market_data
    )


    prices = (
        prices
        .dropna()
    )


    return prices




# =============================================================================
# MARKET SUMMARY
# =============================================================================


def market_summary(
        market_data
):
    """
    Generate quick statistics.
    """


    returns = returns_matrix(
        market_data
    )


    summary = pd.DataFrame({

        "Annual Return":
            returns.mean() * 252,


        "Volatility":
            returns.std() * (252 ** 0.5),


        "Sharpe":
            (
                returns.mean()
                /
                returns.std()
            )
            *
            (252 ** 0.5)

    })


    return summary




# =============================================================================
# TEST
# =============================================================================


if __name__ == "__main__":


    symbols = [

        "RELIANCE.NS",

        "TCS.NS",

        "INFY.NS"

    ]


    data = load_market_data(
        symbols,
        period="2y"
    )


    print("\nLoaded Assets:")

    for stock in data:

        print(
            stock,
            data[stock].shape
        )



    prices = price_matrix(
        data
    )


    print(
        "\nPrice Matrix:"
    )

    print(
        prices.head()
    )



    returns = returns_matrix(
        data
    )


    print(
        "\nReturns:"
    )

    print(
        returns.head()
    )



    print(
        "\nSummary:"
    )

    print(
        market_summary(data)
    )