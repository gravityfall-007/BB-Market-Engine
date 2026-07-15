"""
volatility.py

Risk and volatility analysis engine.

Indicators:

- ATR
- Bollinger Bands
- Historical Volatility
- Volatility Ratio
- Volatility Regime
- Risk Score
"""


import pandas as pd
import numpy as np

# pyrefly: ignore [missing-import]
import ta

import sys
from pathlib import Path

# Allow importing config when running script directly
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

# =============================================================================
# ATR
# =============================================================================


def add_atr(
        df,
        period=14
):
    """
    Average True Range

    Measures price movement range.

    Higher ATR:
        Higher volatility

    """


    indicator = ta.volatility.AverageTrueRange(

        high=df["High"],

        low=df["Low"],

        close=df["Close"],

        window=period

    )


    df["ATR"] = (

        indicator.average_true_range()

    )


    # ATR percentage

    df["ATR_Percent"] = (

        df["ATR"]
        /
        df["Close"]

    ) * 100


    return df




# =============================================================================
# BOLLINGER BANDS
# =============================================================================


def add_bollinger_bands(
        df,
        period=20,
        std=2
):

    """
    Bollinger Bands

    Detect:

    - Overextension
    - Volatility expansion
    - Volatility contraction

    """


    indicator = ta.volatility.BollingerBands(

        close=df["Close"],

        window=period,

        window_dev=std

    )


    df["BB_Upper"] = (

        indicator.bollinger_hband()

    )


    df["BB_Middle"] = (

        indicator.bollinger_mavg()

    )


    df["BB_Lower"] = (

        indicator.bollinger_lband()

    )


    df["BB_Width"] = (

        indicator.bollinger_wband()

    )


    return df




# =============================================================================
# HISTORICAL VOLATILITY
# =============================================================================


def add_historical_volatility(
        df,
        period=20
):

    """
    Annualized historical volatility.

    """


    daily_returns = (

        df["Close"]
        .pct_change()

    )


    df["Historical_Volatility"] = (

        daily_returns
        .rolling(period)
        .std()

        *

        np.sqrt(252)

        *

        100

    )


    return df




# =============================================================================
# VOLATILITY RATIO
# =============================================================================


def add_volatility_ratio(df):

    """
    Current volatility compared
    with long-term volatility.

    """

    df["Volatility_Ratio"] = (

        df["Historical_Volatility"]

        /

        df["Historical_Volatility"]
        .rolling(100)
        .mean()

    )


    return df




# =============================================================================
# VOLATILITY REGIME
# =============================================================================


def volatility_regime(df):

    """
    Market regime:

    0 = Low volatility
    1 = Normal volatility
    2 = High volatility

    """


    df["Volatility_Regime"] = np.where(

        df["Volatility_Ratio"] < 0.8,

        0,

        np.where(

            df["Volatility_Ratio"] > 1.2,

            2,

            1

        )

    )


    return df




# =============================================================================
# RISK SCORE
# =============================================================================


def risk_score(df):

    """
    Risk Score

    Range:
    0-100


    Higher score =
    safer environment


    Components:

    ATR stability       30%
    Bollinger width     25%
    Volatility regime   25%
    Volatility ratio    20%

    """


    score = pd.Series(

        0,

        index=df.index

    )



    # ATR

    score += np.where(

        df["ATR_Percent"] < 3,

        30,

        10

    )



    # Bollinger Width

    score += np.where(

        df["BB_Width"] <

        df["BB_Width"].rolling(100).mean(),

        25,

        10

    )



    # Regime

    score += np.where(

        df["Volatility_Regime"] == 0,

        25,

        np.where(

            df["Volatility_Regime"] == 1,

            15,

            5

        )

    )



    # Ratio

    score += np.where(

        df["Volatility_Ratio"] < 1,

        20,

        5

    )



    df["Risk_Score"] = score


    return df




# =============================================================================
# COMPLETE VOLATILITY PIPELINE
# =============================================================================


def calculate_volatility_indicators(df):

    """
    Execute complete volatility engine.
    """


    df = add_atr(df)

    df = add_bollinger_bands(df)

    df = add_historical_volatility(df)

    df = add_volatility_ratio(df)

    df = volatility_regime(df)

    df = risk_score(df)


    return df




# =============================================================================
# TEST
# =============================================================================


if __name__ == "__main__":


    from data.yahoo import download_symbol


    data = download_symbol(

        "RELIANCE.NS",

        period="5y"

    )


    result = calculate_volatility_indicators(
        data
    )


    print(

        result[

            [
                "Close",
                "ATR",
                "ATR_Percent",
                "Historical_Volatility",
                "Volatility_Regime",
                "Risk_Score"

            ]

        ]

        .tail()

    )