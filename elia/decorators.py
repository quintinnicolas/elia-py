"""
@author: nicolasquintin
"""

from functools import wraps
import pandas as pd
from itertools import tee


def split_in_chunks(freq: str):
    """Attempts to deal with usage restrictions on the API. Since the maximum allowed number of rows per query is 100,
    the query can be broken into separate chunks containing at most 100 rows, for instance data with quarter-hourly
    granularity can be split into daily chunks of 96 rows each. Allowed split frequencies are available here:
    https://pandas.pydata.org/docs/user_guide/timeseries.html#timeseries-offset-aliases"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, start, end, **kwargs):
            dates = pd.date_range(start, end, freq=freq, inclusive="left")
            dates = dates.insert(len(dates), end)
            dfs = []
            for _start, _end in _pairwise(dates):
                df_tmp = func(*args, start=_start, end=_end, **kwargs)
                dfs.append(df_tmp)
            df = pd.concat(dfs)
            df = df.loc[~df.index.duplicated(keep='first')]
            return df

        return wrapper
    return decorator


def _pairwise(iterable):
    # As of python3.10, you can simply import the function pairwise from itertools
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)
