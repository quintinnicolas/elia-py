"""
@author: nicolasquintin
"""
import logging

from functools import wraps
import pandas as pd
from itertools import tee

from constants import DATETIME_FORMAT
from exceptions import TooManyRowsError


def split_along_time(freq: str):
    """Attempts to deal with the restrictions of the API. Since the maximum allowed number of rows per query is 100,
    the query can be broken into separate chunks containing at most 100 rows, for instance data with quarter-hourly
    granularity can be split into daily chunks of 96 rows each. Allowed split frequencies are available here:
    https://pandas.pydata.org/docs/user_guide/timeseries.html#timeseries-offset-aliases"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, start, end, **kwargs):
            # dates = pd.date_range(start, end, freq=freq, inclusive="left")  # Python 3.10
            dates = pd.date_range(start, end, freq=freq, closed="left")  # Python 3.9 or below
            dates = dates.insert(len(dates), end)
            dfs = []
            for _start, _end in _pairwise(dates):
                df_tmp = func(*args, start=_start, end=_end, **kwargs)
                dfs.append(df_tmp)
            df = pd.concat(dfs)
            return df

        return wrapper
    return decorator


def split_in_chunks_if_too_long(chunks: int = 3):
    """Attempts to deal with restrictions of the API. If an TooManyRowsError error is detected, the query is split
    into several pieces"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, start, end, **kwargs):
            try:
                logging.info(f"Querying {func.__qualname__} from {start.strftime(DATETIME_FORMAT)} to {end.strftime(DATETIME_FORMAT)}")
                df = func(*args, start=start, end=end, **kwargs)
            except TooManyRowsError:
                logging.error(f"The query appears to be too long! Attempt to split it into {chunks} chunks")
                dates = pd.date_range(start, end, periods=(chunks+1))  # e.g. 3 chunks require 4 interval points.
                dfs = []
                for _start, _end in _pairwise(dates):
                    df_tmp = decorator(func)(*args, start=_start, end=_end, **kwargs)  # Recursive function :-)
                    dfs.append(df_tmp)
                df = pd.concat(dfs)
            return df
        return wrapper
    return decorator


def _pairwise(iterable):
    # As of python3.10, you can simply import the function pairwise from itertools
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)
