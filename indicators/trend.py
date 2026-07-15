"""
trend.py

Trend analysis engine.

Indicators:
- SMA
- EMA
- Golden Cross
- Death Cross
- ADX
- SuperTrend
- Trend Score
"""


import sys
from pathlib import Path

# Allow importing config when running script directly
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pandas as pd
import numpy as np
import ta


from config import (
    EMA_FAST,
    EMA_SLOW,
    LONG_TREND,
    ADX_PERIOD,
    SUPERTREND_PERIOD,
    SUPERTREND_MULTIPLIER
)



# =============================================================================
# SIMPLE MOVING AVERAGE
# =============================================================================


def sma(
        df: pd.DataFrame,
        period: int
):

    """
    Calculate Simple Moving Average
    """


    df[f"SMA_{period}"] = (

        df["Close"]
        .rolling(period)
        .mean()

    )


    return df



# =============================================================================
# EXPONENTIAL MOVING AVERAGE
# =============================================================================


def ema(
        df: pd.DataFrame,
        period: int
):

    """
    Calculate EMA
    """


    df[f"EMA_{period}"] = (

        df["Close"]
        .ewm(
            span=period,
            adjust=False
        )
        .mean()

    )


    return df



# =============================================================================
# MOVING AVERAGE SYSTEM
# =============================================================================


def moving_average_system(df):

    """
    Add:
    - Fast EMA
    - Slow EMA
    - Long-term trend
    """


    df = ema(
        df,
        EMA_FAST
    )


    df = ema(
        df,
        EMA_SLOW
    )


    df = sma(
        df,
        LONG_TREND
    )


    return df



# =============================================================================
# GOLDEN CROSS / DEATH CROSS
# =============================================================================


def moving_average_signal(df):

    """
    Golden Cross:

    EMA20 crosses above EMA50

    Death Cross:

    EMA20 crosses below EMA50
    """


    df["MA_Signal"] = 0



    df.loc[

        df[f"EMA_{EMA_FAST}"]
        >
        df[f"EMA_{EMA_SLOW}"],

        "MA_Signal"

    ] = 1



    df["MA_Crossover"] = (

        df["MA_Signal"]
        .diff()

    )



    return df




# =============================================================================
# TREND DIRECTION
# =============================================================================


def trend_direction(df):

    """
    Determine market trend

    1  = Bullish
    0  = Neutral
    -1 = Bearish

    """


    conditions = [

        (
            df["Close"]
            >
            df[f"SMA_{LONG_TREND}"]
        ),

        (
            df[f"EMA_{EMA_FAST}"]
            >
            df[f"EMA_{EMA_SLOW}"]
        )

    ]


    df["Trend"] = np.where(

        conditions[0]
        &
        conditions[1],

        1,

        np.where(

            df["Close"]
            <
            df[f"SMA_{LONG_TREND}"],

            -1,

            0
        )

    )


    return df




# =============================================================================
# ADX
# =============================================================================


def add_adx(df):

    """
    Average Directional Index

    Measures trend strength.

    >25 strong trend
    <20 weak trend

    """


    indicator = ta.trend.ADXIndicator(

        high=df["High"],

        low=df["Low"],

        close=df["Close"],

        window=ADX_PERIOD

    )


    df["ADX"] = (

        indicator.adx()

    )


    return df




# =============================================================================
# SUPERTREND
# =============================================================================


def supertrend(df):

    """
    SuperTrend indicator

    Uses ATR volatility.
    """


    atr = ta.volatility.AverageTrueRange(

        high=df["High"],

        low=df["Low"],

        close=df["Close"],

        window=SUPERTREND_PERIOD

    )


    df["ATR"] = atr.average_true_range()



    middle = (

        df["High"]
        +
        df["Low"]

    ) / 2



    upper_band = (

        middle
        +
        (
            SUPERTREND_MULTIPLIER
            *
            df["ATR"]
        )

    )



    lower_band = (

        middle
        -
        (
            SUPERTREND_MULTIPLIER
            *
            df["ATR"]
        )

    )



    df["SuperTrend"] = np.nan


    df.loc[

        df["Close"]
        >
        upper_band,

        "SuperTrend"

    ] = 1



    df.loc[

        df["Close"]
        <
        lower_band,

        "SuperTrend"

    ] = -1



    df["SuperTrend"] = (

        df["SuperTrend"]
        .ffill()

    )


    return df




# =============================================================================
# TREND SCORE
# =============================================================================


def trend_score(df):

    """
    Bull Market Engine Trend Score

    Range:
    0 - 100

    Components:

    EMA alignment       40%
    Price vs 200 SMA    30%
    ADX strength        20%
    SuperTrend          10%

    """


    score = pd.Series(

        0,

        index=df.index

    )


    # EMA

    score += np.where(

        df[f"EMA_{EMA_FAST}"]
        >
        df[f"EMA_{EMA_SLOW}"],

        40,

        0

    )


    # Long term trend

    score += np.where(

        df["Close"]
        >
        df[f"SMA_{LONG_TREND}"],

        30,

        0

    )


    # ADX

    score += np.where(

        df["ADX"]
        >
        25,

        20,

        0

    )


    # SuperTrend

    score += np.where(

        df["SuperTrend"]
        ==

        1,

        10,

        0

    )



    df["Trend_Score"] = score


    return df




# =============================================================================
# COMPLETE TREND PIPELINE
# =============================================================================


def calculate_trend_indicators(df):

    """
    Execute complete trend engine.
    """


    df = moving_average_system(df)

    df = moving_average_signal(df)

    df = trend_direction(df)

    df = add_adx(df)

    df = supertrend(df)

    df = trend_score(df)


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


    result = calculate_trend_indicators(
        data
    )


    print(

        result[
            [
                "Close",
                "EMA_20",
                "EMA_50",
                "ADX",
                "SuperTrend",
                "Trend_Score"
            ]
        ]
        .tail()

    )