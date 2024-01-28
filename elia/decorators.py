"""
@author: nicolasquintin
"""
from __future__ import annotations

import datetime as dt
from itertools import tee
from functools import wraps
from typing import Callable, Any, Iterable

import pandas as pd


def split_along_time(freq: str) -> Callable:
    """Splits the query into multiple sub queries, with smaller time windows. Allowed split frequencies are
    available here: https://pandas.pydata.org/docs/user_guide/timeseries.html#timeseries-offset-aliases"""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(
                *args: Any,
                start: dt.datetime | dt.date | pd.Timestamp,
                end: dt.datetime | dt.date | pd.Timestamp,
                **kwargs: Any) -> pd.DataFrame:
            dates = pd.date_range(start, end, freq=freq, inclusive="left")
            if len(dates) == 0:
                dates = dates.insert(len(dates), start)
            dates = dates.insert(len(dates), end)
            dfs = []
            for _start, _end in _pairwise(dates):
                df_tmp = func(*args, start=_start, end=_end, **kwargs)
                dfs.append(df_tmp)
            df = pd.concat(dfs)
            return df

        return wrapper
    return decorator


def _pairwise(iterable: Iterable) -> zip:
    # As of python3.10, you can simply import the function pairwise from itertools
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)
