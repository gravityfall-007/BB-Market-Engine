"""
strength.py

Relative strength analysis engine.

Indicators:

- Relative Strength vs Benchmark
- Alpha
- Beta
- Sharpe Ratio
- Information Ratio
- Rolling Relative Strength
- Strength Score
"""


import pandas as pd
import numpy as np

import sys
from pathlib import Path

# Allow importing config when running script directly
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from config import (
    RISK_FREE_RATE
)



# =============================================================================
# RELATIVE STRENGTH
# =============================================================================


def add_relative_strength(
        df,
        benchmark_df
):
    """
    Compare stock performance
    against benchmark.

    Formula:

    Stock Return /
    Benchmark Return

    >1 means outperforming

    """


    stock_return = (

        df["Close"]
        /
        df["Close"].iloc[0]

    )


    benchmark_return = (

        benchmark_df["Close"]
        /
        benchmark_df["Close"].iloc[0]

    )


    df["Relative_Strength"] = (

        stock_return
        /
        benchmark_return

    )


    return df




# =============================================================================
# RELATIVE PERFORMANCE
# =============================================================================


def add_relative_performance(
        df,
        benchmark_df,
        period=252
):

    """
    One year relative performance.

    Positive:
        Outperforming

    Negative:
        Underperforming

    """


    stock_return = (

        df["Close"]
        .pct_change(period)

    )


    benchmark_return = (

        benchmark_df["Close"]
        .pct_change(period)

    )


    df["Relative_Performance"] = (

        stock_return
        -
        benchmark_return

    )


    return df




# =============================================================================
# BETA
# =============================================================================


def add_beta(
        df,
        benchmark_df,
        period=252
):

    """
    Market sensitivity.

    Beta > 1:
        More volatile than market

    Beta < 1:
        Defensive

    """


    stock_returns = (

        df["Close"]
        .pct_change()

    )


    market_returns = (

        benchmark_df["Close"]
        .pct_change()

    )


    covariance = (

        stock_returns
        .rolling(period)
        .cov(
            market_returns
        )

    )


    market_variance = (

        market_returns
        .rolling(period)
        .var()

    )


    df["Beta"] = (

        covariance
        /
        market_variance

    )


    return df




# =============================================================================
# ALPHA
# =============================================================================


def add_alpha(
        df,
        benchmark_df,
        period=252
):

    """
    Jensen's Alpha


    Alpha =
    Stock return -
    Expected market return

    """


    stock_returns = (

        df["Close"]
        .pct_change()

    )


    market_returns = (

        benchmark_df["Close"]
        .pct_change()

    )


    beta = (

        stock_returns
        .rolling(period)
        .cov(
            market_returns
        )

        /

        market_returns
        .rolling(period)
        .var()

    )


    expected_return = (

        RISK_FREE_RATE

        +

        beta *
        (
            market_returns
            -
            RISK_FREE_RATE
        )

    )


    df["Alpha"] = (

        stock_returns
        -
        expected_return

    )


    return df




# =============================================================================
# SHARPE RATIO
# =============================================================================


def add_sharpe_ratio(
        df,
        period=252
):

    """
    Risk adjusted return.
    """


    returns = (

        df["Close"]
        .pct_change()

    )


    excess_return = (

        returns
        -
        RISK_FREE_RATE / period

    )


    df["Sharpe_Ratio"] = (

        excess_return
        .rolling(period)
        .mean()

        /

        excess_return
        .rolling(period)
        .std()

    ) * np.sqrt(period)



    return df




# =============================================================================
# INFORMATION RATIO
# =============================================================================


def add_information_ratio(
        df,
        benchmark_df,
        period=252
):

    """
    Measures consistency of outperformance.
    """


    stock_returns = (

        df["Close"]
        .pct_change()

    )


    benchmark_returns = (

        benchmark_df["Close"]
        .pct_change()

    )


    active_return = (

        stock_returns
        -
        benchmark_returns

    )


    df["Information_Ratio"] = (

        active_return
        .rolling(period)
        .mean()

        /

        active_return
        .rolling(period)
        .std()

    ) * np.sqrt(period)



    return df




# =============================================================================
# STRENGTH SCORE
# =============================================================================


def strength_score(df):

    """
    Relative Strength Score

    Range:

    0 - 100


    Components:

    Relative strength       35%
    Alpha                   20%
    Sharpe                  20%
    Information ratio       15%
    Beta                    10%

    """


    score = pd.Series(
        0,
        index=df.index
    )


    # Relative strength

    score += np.where(

        df["Relative_Strength"] > 1,

        35,

        0

    )


    # Alpha

    score += np.where(

        df["Alpha"] > 0,

        20,

        0

    )


    # Sharpe

    score += np.where(

        df["Sharpe_Ratio"] > 1,

        20,

        0

    )


    # Information Ratio

    score += np.where(

        df["Information_Ratio"] > 0,

        15,

        0

    )


    # Beta

    score += np.where(

        (df["Beta"] > 0.8)
        &
        (df["Beta"] < 1.5),

        10,

        0

    )


    df["Strength_Score"] = score


    return df




# =============================================================================
# COMPLETE STRENGTH PIPELINE
# =============================================================================


def calculate_strength_indicators(
        df,
        benchmark_df
):

    """
    Execute complete strength engine.
    """


    df = add_relative_strength(
        df,
        benchmark_df
    )


    df = add_relative_performance(
        df,
        benchmark_df
    )


    df = add_beta(
        df,
        benchmark_df
    )


    df = add_alpha(
        df,
        benchmark_df
    )


    df = add_sharpe_ratio(
        df
    )


    df = add_information_ratio(
        df,
        benchmark_df
    )


    df = strength_score(
        df
    )


    return df




# =============================================================================
# TEST
# =============================================================================


if __name__ == "__main__":


    from data.yahoo import download_symbol


    stock = download_symbol(
        "RELIANCE.NS",
        period="5y"
    )


    benchmark = download_symbol(
        "^NSEI",
        period="5y"
    )


    result = calculate_strength_indicators(
        stock,
        benchmark
    )


    print(

        result[
            [
                "Close",
                "Relative_Strength",
                "Beta",
                "Alpha",
                "Sharpe_Ratio",
                "Strength_Score"
            ]
        ]
        .tail()

    )