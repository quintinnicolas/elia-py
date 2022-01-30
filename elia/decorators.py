"""
@author: nicolasquintin
"""
from itertools import tee
from functools import wraps

import pandas as pd


def split_along_time(freq: str):
    """Splits the query into multiple sub queries, with smaller time windows. Allowed split frequencies are
    available here: https://pandas.pydata.org/docs/user_guide/timeseries.html#timeseries-offset-aliases"""
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


def _pairwise(iterable):
    # As of python3.10, you can simply import the function pairwise from itertools
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)
