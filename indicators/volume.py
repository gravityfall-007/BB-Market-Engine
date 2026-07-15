"""
volume.py

Volume analysis engine.

Indicators:
- Volume Moving Average
- Volume Ratio
- Volume Spike
- OBV
- Chaikin Money Flow
- Money Flow Index
- Accumulation Distribution
- Volume Score
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
# VOLUME MOVING AVERAGE
# =============================================================================


def add_volume_average(
        df,
        period=20
):
    """
    Calculate average trading volume.
    """


    df["Volume_MA"] = (

        df["Volume"]
        .rolling(period)
        .mean()

    )


    return df



# =============================================================================
# VOLUME RATIO
# =============================================================================


def add_volume_ratio(df):

    """
    Current volume compared
    with average volume.

    >1  higher than normal
    >2  volume spike

    """


    df["Volume_Ratio"] = (

        df["Volume"]
        /
        df["Volume_MA"]

    )


    return df



# =============================================================================
# VOLUME SPIKE
# =============================================================================


def add_volume_spike(
        df,
        threshold=1.5
):

    """
    Detect unusual volume activity.

    """

    df["Volume_Spike"] = np.where(

        df["Volume_Ratio"]
        >= threshold,

        1,

        0

    )


    return df



# =============================================================================
# ON BALANCE VOLUME
# =============================================================================


def add_obv(df):

    """
    On Balance Volume

    Measures buying/selling pressure.
    """


    indicator = ta.volume.OnBalanceVolumeIndicator(

        close=df["Close"],

        volume=df["Volume"]

    )


    df["OBV"] = (

        indicator.on_balance_volume()

    )


    return df



# =============================================================================
# CHAikin MONEY FLOW
# =============================================================================


def add_cmf(df):

    """
    Chaikin Money Flow

    Positive:
        Accumulation

    Negative:
        Distribution

    """


    indicator = ta.volume.ChaikinMoneyFlowIndicator(

        high=df["High"],

        low=df["Low"],

        close=df["Close"],

        volume=df["Volume"]

    )


    df["CMF"] = (

        indicator.chaikin_money_flow()

    )


    return df



# =============================================================================
# MONEY FLOW INDEX
# =============================================================================


def add_mfi(df):

    """
    Money Flow Index

    Similar to RSI but volume weighted.

    >80 Overbought
    <20 Oversold

    """


    indicator = ta.volume.MFIIndicator(

        high=df["High"],

        low=df["Low"],

        close=df["Close"],

        volume=df["Volume"]

    )


    df["MFI"] = (

        indicator.money_flow_index()

    )


    return df



# =============================================================================
# ACCUMULATION DISTRIBUTION
# =============================================================================


def add_accumulation_distribution(df):

    """
    Accumulation Distribution Line

    Detects institutional accumulation.
    """


    indicator = ta.volume.AccDistIndexIndicator(

        high=df["High"],

        low=df["Low"],

        close=df["Close"],

        volume=df["Volume"]

    )


    df["AD_Line"] = (

        indicator.acc_dist_index()

    )


    return df




# =============================================================================
# VOLUME SCORE
# =============================================================================


def volume_score(df):

    """
    Bull Market Volume Score

    Range:
    0 - 100


    Components:

    Volume Ratio       25%
    Volume Spike       20%
    OBV Trend          25%
    CMF                20%
    MFI                10%

    """


    score = pd.Series(

        0,

        index=df.index

    )



    # ------------------------------------
    # Volume Ratio
    # ------------------------------------


    score += np.where(

        df["Volume_Ratio"] > 1,

        25,

        0

    )



    # ------------------------------------
    # Volume Spike
    # ------------------------------------


    score += np.where(

        df["Volume_Spike"] == 1,

        20,

        0

    )



    # ------------------------------------
    # OBV trend
    # ------------------------------------


    obv_change = (

        df["OBV"]
        .diff()

    )


    score += np.where(

        obv_change > 0,

        25,

        0

    )



    # ------------------------------------
    # Chaikin Money Flow
    # ------------------------------------


    score += np.where(

        df["CMF"] > 0,

        20,

        0

    )



    # ------------------------------------
    # MFI
    # ------------------------------------


    score += np.where(

        (df["MFI"] > 40)
        &
        (df["MFI"] < 80),

        10,

        0

    )



    df["Volume_Score"] = score


    return df



# =============================================================================
# COMPLETE VOLUME PIPELINE
# =============================================================================


def calculate_volume_indicators(df):

    """
    Execute complete volume engine.
    """


    df = add_volume_average(df)

    df = add_volume_ratio(df)

    df = add_volume_spike(df)

    df = add_obv(df)

    df = add_cmf(df)

    df = add_mfi(df)

    df = add_accumulation_distribution(df)

    df = volume_score(df)


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


    result = calculate_volume_indicators(
        data
    )


    print(

        result[

            [
                "Close",
                "Volume",
                "Volume_Ratio",
                "OBV",
                "CMF",
                "MFI",
                "Volume_Score"

            ]

        ]

        .tail()

    )