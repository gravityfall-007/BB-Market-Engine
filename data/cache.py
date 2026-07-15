"""
cache.py

Caching engine for Bull Market Engine.

Handles:
- Market data caching
- Expiration checks
- Cache management
- Cache statistics
"""


import os
import json
import shutil

from pathlib import Path
from datetime import datetime, timedelta

import sys
import pandas as pd
import yfinance as yf

# Allow importing config when running script directly
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))


from config import (
    CACHE_DIR,
    CACHE_EXPIRY_HOURS
)



# =============================================================================
# CACHE METADATA
# =============================================================================


CACHE_META_FILE = CACHE_DIR / "cache_metadata.json"



def load_metadata():

    """
    Load cache metadata
    """

    if not CACHE_META_FILE.exists():

        return {}

    with open(
        CACHE_META_FILE,
        "r"
    ) as file:

        return json.load(file)




def save_metadata(metadata):

    """
    Save cache metadata
    """

    with open(
        CACHE_META_FILE,
        "w"
    ) as file:

        json.dump(
            metadata,
            file,
            indent=4,
            default=str
        )



# =============================================================================
# CACHE REGISTRATION
# =============================================================================


def register_cache(
        filename: str,
        symbol: str,
        interval: str
):
    """
    Register downloaded data
    """


    metadata = load_metadata()


    metadata[filename] = {

        "symbol": symbol,

        "interval": interval,

        "created":

            datetime.now()

    }


    save_metadata(metadata)




# =============================================================================
# CHECK CACHE VALIDITY
# =============================================================================


def is_cache_valid(filename: str):

    """
    Check whether cached data is still usable

    Returns:
        True  -> cache valid
        False -> download required
    """


    path = CACHE_DIR / filename


    if not path.exists():

        return False



    modified_time = datetime.fromtimestamp(
        path.stat().st_mtime
    )


    expiry_time = (
        datetime.now()
        -
        timedelta(
            hours=CACHE_EXPIRY_HOURS
        )
    )


    return modified_time > expiry_time




# =============================================================================
# GET CACHE FILE
# =============================================================================


def get_cache_file(filename):

    """
    Return cache path
    """

    path = CACHE_DIR / filename


    if path.exists():

        return path


    return None




# =============================================================================
# DELETE CACHE
# =============================================================================


def clear_cache():

    """
    Remove all cached files
    """


    for item in CACHE_DIR.iterdir():

        if item.is_file():

            item.unlink()


        elif item.is_dir():

            shutil.rmtree(item)



    print(
        "Cache cleared successfully"
    )



# =============================================================================
# CACHE SIZE
# =============================================================================


def cache_size():

    """
    Calculate cache size
    """

    total = 0


    for file in CACHE_DIR.rglob("*"):

        if file.is_file():

            total += file.stat().st_size



    return round(
        total / (1024 ** 2),
        2
    )



# =============================================================================
# CACHE REPORT
# =============================================================================


def cache_report():

    """
    Display cache information
    """


    metadata = load_metadata()


    print(
        "\n====== CACHE REPORT ======\n"
    )


    print(
        "Files:",
        len(metadata)
    )


    print(
        "Size:",
        cache_size(),
        "MB"
    )


    for file, info in metadata.items():

        print(
            f"""
File:
{file}

Symbol:
{info['symbol']}

Interval:
{info['interval']}

Created:
{info['created']}

-------------------------
"""
        )



# =============================================================================
# TEST
# =============================================================================


if __name__ == "__main__":


    print(
        "Cache directory:",
        CACHE_DIR
    )


    cache_report()
    clear_cache()