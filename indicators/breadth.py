"""
breadth.py

Market breadth analysis engine.

Measures overall market participation.

Indicators:

- Advance Decline Ratio
- Stocks Above Moving Averages
- New High/New Low Ratio
- Participation Score
- Market Regime
"""


import pandas as pd
import numpy as np
import sys
from pathlib import Path

# Allow importing config when running script directly
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))


# =============================================================================
# ADVANCE DECLINE RATIO
# =============================================================================


def advance_decline_ratio(
        market_data
):
    """
    Calculate market advance decline ratio.


    market_data example:

    {
        "TCS.NS": dataframe,
        "INFY.NS": dataframe
    }


    Returns:

    DataFrame

    Date | Advance | Decline | Ratio

    """


    advances = []

    declines = []


    dates = list(

        market_data.values()

    )[0].index



    for date in dates:


        advance = 0

        decline = 0


        for stock in market_data.values():


            try:

                today = stock.loc[
                    date,
                    "Close"
                ]

                previous = stock.loc[
                    date
                ].shift(1)["Close"]



                if today > previous:

                    advance += 1


                elif today < previous:

                    decline += 1


            except:

                continue



        advances.append(
            advance
        )


        declines.append(
            decline
        )



    result = pd.DataFrame(

        {

            "Advances": advances,

            "Declines": declines

        },

        index=dates

    )


    result["AD_Ratio"] = (

        result["Advances"]

        /

        result["Declines"]
        .replace(0,1)

    )


    return result




# =============================================================================
# STOCKS ABOVE MOVING AVERAGE
# =============================================================================


def percentage_above_ma(
        market_data,
        period=200
):

    """
    Percentage of stocks trading
    above moving average.

    Example:

    80% above 200 SMA
    means strong market breadth.

    """


    result = []

    dates = list(
        market_data.values()
    )[0].index



    for date in dates:


        total = 0

        above = 0



        for stock in market_data.values():


            try:

                history = (

                    stock.loc[:date]

                )


                if len(history) < period:

                    continue



                ma = (

                    history["Close"]

                    .rolling(period)

                    .mean()

                    .iloc[-1]

                )


                price = (

                    history["Close"]

                    .iloc[-1]

                )


                total += 1


                if price > ma:

                    above += 1


            except:

                continue



        percentage = (

            above / total * 100

            if total > 0

            else 0

        )


        result.append(
            percentage
        )



    return pd.DataFrame(

        {

            f"Above_{period}_SMA":

            result

        },

        index=dates

    )




# =============================================================================
# NEW HIGH NEW LOW RATIO
# =============================================================================


def high_low_ratio(
        market_data,
        period=252
):

    """
    New 52 week highs vs lows.

    Strong bull market:

    More highs than lows.

    """


    dates = list(
        market_data.values()
    )[0].index


    highs = []

    lows = []



    for date in dates:


        high_count = 0

        low_count = 0



        for stock in market_data.values():


            try:

                history = stock.loc[:date]


                if len(history) < period:

                    continue



                price = (

                    history["Close"]
                    .iloc[-1]

                )


                high = (

                    history["Close"]
                    .rolling(period)
                    .max()
                    .iloc[-1]

                )


                low = (

                    history["Close"]
                    .rolling(period)
                    .
                    min()
                    .iloc[-1]

                )


                if price >= high:

                    high_count += 1


                if price <= low:

                    low_count += 1



            except:

                continue



        highs.append(
            high_count
        )


        lows.append(
            low_count
        )



    result = pd.DataFrame(

        {

            "New_Highs": highs,

            "New_Lows": lows

        },

        index=dates

    )


    result["High_Low_Ratio"] = (

        result["New_Highs"]

        /

        result["New_Lows"]
        .replace(0,1)

    )


    return result




# =============================================================================
# PARTICIPATION SCORE
# =============================================================================


def participation_score(
        breadth_df
):

    """
    Market Breadth Score

    Range:

    0-100


    Components:

    Advance Decline 40%

    Above 200 SMA 40%

    New High/Lows 20%

    """


    score = pd.Series(

        0,

        index=breadth_df.index

    )



    # Advance decline

    score += np.where(

        breadth_df["AD_Ratio"] > 1,

        40,

        0

    )



    # Moving average breadth

    score += np.where(

        breadth_df["Above_200_SMA"] > 50,

        40,

        0

    )



    # High low

    score += np.where(

        breadth_df["High_Low_Ratio"] > 1,

        20,

        0

    )


    breadth_df["Breadth_Score"] = score


    return breadth_df




# =============================================================================
# MARKET REGIME
# =============================================================================


def market_regime(
        breadth_df
):

    """
    Market state:


    2 = Bull Market

    1 = Neutral

    0 = Bear Market

    """


    breadth_df["Market_Regime"] = np.where(

        breadth_df["Breadth_Score"] >= 70,

        2,


        np.where(

            breadth_df["Breadth_Score"] >= 40,

            1,

            0

        )

    )


    return breadth_df




# =============================================================================
# COMPLETE BREADTH PIPELINE
# =============================================================================


def calculate_breadth(
        market_data
):

    """
    Complete market breadth engine.
    """


    ad = advance_decline_ratio(
        market_data
    )


    ma = percentage_above_ma(
        market_data,
        200
    )


    hl = high_low_ratio(
        market_data
    )


    breadth = (

        ad

        .join(ma)

        .join(hl)

    )


    breadth = participation_score(
        breadth
    )


    breadth = market_regime(
        breadth
    )


    return breadth




# =============================================================================
# TEST
# =============================================================================


if __name__ == "__main__":


    from data.loader import load_market_data



    stocks = [

        "RELIANCE.NS",

        "TCS.NS",

        "INFY.NS",

        "HDFCBANK.NS",

        "ICICIBANK.NS"

    ]


    market = load_market_data(
        stocks,
        period="5y"
    )


    result = calculate_breadth(
        market
    )


    print(

        result.tail()

    )