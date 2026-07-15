"""
momentum.py

Momentum analysis engine.

Indicators:
- RSI
- MACD
- ROC
- Stochastic Oscillator
- Williams %R
- Momentum Score
"""


import pandas as pd
import numpy as np

# pyrefly: ignore [missing-import]
import ta
import sys
from pathlib import Path

# Allow importing config when running script directly
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from config import (
    RSI_PERIOD,
    MACD_FAST,
    MACD_SLOW,
    MACD_SIGNAL
)



# =============================================================================
# RSI
# =============================================================================


def add_rsi(
        df: pd.DataFrame,
        period: int = RSI_PERIOD
):
    """
    Relative Strength Index

    Interpretation:

    RSI > 70  : Overbought
    RSI < 30  : Oversold
    """


    indicator = ta.momentum.RSIIndicator(

        close=df["Close"],

        window=period

    )


    df["RSI"] = (
        indicator.rsi()
    )


    return df




# =============================================================================
# MACD
# =============================================================================


def add_macd(df):

    """
    Moving Average Convergence Divergence

    Bullish:
    MACD > Signal

    Bearish:
    MACD < Signal

    """


    macd = ta.trend.MACD(

        close=df["Close"],

        window_fast=MACD_FAST,

        window_slow=MACD_SLOW,

        window_sign=MACD_SIGNAL

    )


    df["MACD"] = (
        macd.macd()
    )


    df["MACD_Signal"] = (
        macd.macd_signal()
    )


    df["MACD_Histogram"] = (
        macd.macd_diff()
    )


    return df




# =============================================================================
# RATE OF CHANGE
# =============================================================================


def add_roc(
        df,
        period=12
):

    """
    Rate of Change

    Measures percentage price momentum.
    """


    roc = ta.momentum.ROCIndicator(

        close=df["Close"],

        window=period

    )


    df["ROC"] = (
        roc.roc()
    )


    return df




# =============================================================================
# STOCHASTIC OSCILLATOR
# =============================================================================


def add_stochastic(df):

    """
    Stochastic oscillator

    %K and %D lines

    """


    stochastic = ta.momentum.StochasticOscillator(

        high=df["High"],

        low=df["Low"],

        close=df["Close"]

    )


    df["STOCH_K"] = (
        stochastic.stoch()
    )


    df["STOCH_D"] = (
        stochastic.stoch_signal()
    )


    return df




# =============================================================================
# WILLIAMS %R
# =============================================================================


def add_williams_r(df):

    """
    Williams %R indicator

    Range:

    -20  -> Overbought
    -80  -> Oversold

    """


    indicator = ta.momentum.WilliamsRIndicator(

        high=df["High"],

        low=df["Low"],

        close=df["Close"]

    )


    df["Williams_R"] = (

        indicator.williams_r()

    )


    return df




# =============================================================================
# MOMENTUM SCORE
# =============================================================================


def momentum_score(df):

    """
    Bull Market Momentum Score

    Range:
    0 - 100


    Components:

    RSI              30%
    MACD             30%
    ROC              20%
    Stochastic       10%
    Williams %R      10%

    """


    score = pd.Series(

        0,

        index=df.index

    )



    # --------------------------------------------------
    # RSI
    # --------------------------------------------------

    score += np.where(

        (df["RSI"] > 50)
        &
        (df["RSI"] < 70),

        30,

        np.where(

            df["RSI"] >= 70,

            15,

            0
        )

    )



    # --------------------------------------------------
    # MACD
    # --------------------------------------------------

    score += np.where(

        df["MACD"]
        >
        df["MACD_Signal"],

        30,

        0

    )



    # --------------------------------------------------
    # ROC
    # --------------------------------------------------

    score += np.where(

        df["ROC"] > 0,

        20,

        0

    )



    # --------------------------------------------------
    # Stochastic
    # --------------------------------------------------

    score += np.where(

        df["STOCH_K"]
        >
        df["STOCH_D"],

        10,

        0

    )



    # --------------------------------------------------
    # Williams R
    # --------------------------------------------------

    score += np.where(

        df["Williams_R"]
        >
        -50,

        10,

        0

    )


    df["Momentum_Score"] = score


    return df




# =============================================================================
# COMPLETE MOMENTUM PIPELINE
# =============================================================================


def calculate_momentum_indicators(df):

    """
    Execute complete momentum engine.
    """


    df = add_rsi(df)

    df = add_macd(df)

    df = add_roc(df)

    df = add_stochastic(df)

    df = add_williams_r(df)

    df = momentum_score(df)


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


    result = calculate_momentum_indicators(
        data
    )


    print(

        result[
            [
                "Close",
                "RSI",
                "MACD",
                "MACD_Signal",
                "ROC",
                "Momentum_Score"
            ]
        ]
        .tail()

    )