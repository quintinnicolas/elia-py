"""
@author: nicolasquintin
"""

import pandas as pd
from elia.get_consumption import load_forecast_1

if __name__ == "__main__":
    dtime_start = pd.to_datetime('20210101', format='%Y%m%d')
    dtime_end = pd.to_datetime('20210201', format='%Y%m%d')

    start = str(dtime_start.date())
    end = str(dtime_end.date())
    df = load_forecast_1(start, end)
    print(df)
