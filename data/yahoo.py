"""
Yahoo Finance Data Provider

Downloads and manages historical market data
for Bull Market Engine.
"""


import os
import time
from pathlib import Path
from typing import Union, List

import sys
import pandas as pd
import yfinance as yf

# Allow importing config when running script directly
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from config import (
    CACHE_DIR,
    DEFAULT_PERIOD,
    DEFAULT_INTERVAL,
    CACHE_ENABLED,
)


# =============================================================================
# CACHE PATH
# =============================================================================


def _cache_path(symbol: str, interval: str) -> Path:
    """
    Generate cache filename
    """

    filename = (
        f"{symbol.replace('.', '_')}"
        f"_{interval}.csv"
    )

    return CACHE_DIR / filename



# =============================================================================
# DOWNLOAD SINGLE ASSET
# =============================================================================


def download_symbol(
        symbol: str,
        period: str = DEFAULT_PERIOD,
        interval: str = DEFAULT_INTERVAL,
        force_refresh: bool = False,
        retries: int = 3
):
    """
    Download historical OHLCV data.

    Parameters
    ----------
    symbol:
        Yahoo Finance ticker

        Examples:
        RELIANCE.NS
        TCS.NS
        AAPL

    period:
        Data history

        Example:
        5y
        1y
        max

    interval:
        Candle interval

        Example:
        1d
        1h
        15m

    Returns
    -------
    pandas.DataFrame

    """


    cache_file = _cache_path(
        symbol,
        interval
    )


    # --------------------------------------------------
    # Load cache
    # --------------------------------------------------

    if (
        CACHE_ENABLED
        and cache_file.exists()
        and not force_refresh
    ):

        df = pd.read_csv(
            cache_file,
            index_col=0,
            parse_dates=True
        )

        return df



    # --------------------------------------------------
    # Download with retry
    # --------------------------------------------------

    for attempt in range(retries):

        try:

            df = yf.download(
                symbol,
                period=period,
                interval=interval,
                auto_adjust=False,
                progress=False
            )


            if df.empty:

                raise ValueError(
                    f"No data found for {symbol}"
                )


            break


        except Exception as error:

            print(
                f"Download failed {symbol}"
                f" attempt {attempt+1}/{retries}"
            )

            time.sleep(2)



    else:

        raise RuntimeError(
            f"Unable to download {symbol}"
        )



    # --------------------------------------------------
    # Cleaning
    # --------------------------------------------------

    df = clean_data(df)



    # --------------------------------------------------
    # Save cache
    # --------------------------------------------------

    if CACHE_ENABLED:

        df.to_csv(cache_file)



    return df




# =============================================================================
# MULTIPLE SYMBOL DOWNLOAD
# =============================================================================


def download_symbols(
        symbols: List[str],
        period: str = DEFAULT_PERIOD,
        interval: str = DEFAULT_INTERVAL
):
    """
    Download multiple assets.

    Returns
    -------
    Dictionary:

    {
      "RELIANCE.NS": dataframe,
      "TCS.NS": dataframe
    }

    """


    data = {}


    for symbol in symbols:


        print(
            f"Downloading {symbol}"
        )


        data[symbol] = download_symbol(
            symbol,
            period,
            interval
        )


    return data




# =============================================================================
# DATA CLEANING
# =============================================================================


def clean_data(df: pd.DataFrame):

    """
    Standardize market data
    """


    # Remove empty rows

    df = df.dropna()



    # Flatten multi-index from yfinance

    if isinstance(
        df.columns,
        pd.MultiIndex
    ):

        df.columns = (
            df.columns
            .get_level_values(0)
        )



    # Ensure datetime index

    df.index = pd.to_datetime(
        df.index
    )


    # Sort

    df = df.sort_index()



    # Add returns

    df["Returns"] = (
        df["Adj Close"]
        .pct_change()
    )


    # Log returns

    df["Log_Returns"] = (
        (
            df["Adj Close"]
            /
            df["Adj Close"].shift(1)
        )
        .apply(
            lambda x: None
            if pd.isna(x)
            else __import__("numpy").log(x)
        )
    )



    return df.dropna()




# =============================================================================
# GET LATEST PRICE
# =============================================================================


def latest_price(symbol: str):

    """
    Return current price
    """


    ticker = yf.Ticker(symbol)


    price = ticker.history(
        period="1d"
    )


    return float(
        price["Close"].iloc[-1]
    )




# =============================================================================
# COMPANY INFORMATION
# =============================================================================


def company_info(symbol: str):

    """
    Retrieve company metadata
    """

    ticker = yf.Ticker(symbol)

    return ticker.info



# =============================================================================
# TEST
# =============================================================================


if __name__ == "__main__":


    stock = "AAPL"


    df = download_symbol(
        stock
    )


    print(df.tail())


    print(
        "Latest price:",
        latest_price(stock)
    )