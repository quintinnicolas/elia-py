"""
@author: nicolasquintin
"""
import urllib.request
import json
import re
import pandas as pd
import ssl

from elia import URL_IMBALANCE, R3, R3_STD, R3_FLEX, R2_UP, R2_DOWN, IGCC_DOWN, IGCC_UP, BIDS_DOWN, BIDS_UP, AFRR, MFRR
from elia.utils_elia import adapt_for_timezone


def imbalance_raw_data(utc=False):
    context = ssl.SSLContext()
    with urllib.request.urlopen(URL_IMBALANCE, context=context) as url:
        json_data = json.loads(url.read().decode())

        for m in json_data:
            timestamp_utc = re.split('\(|\)', m["Time"])[1][:10]
            date = pd.Timestamp.utcfromtimestamp(int(timestamp_utc))
            if not utc:
                m["Time"] = adapt_for_timezone(date)
            else:
                m["Time"] = date
    return json_data


def imbalance_dataframe(json_data):
    df = pd.json_normalize(json_data, 'Measurements', 'Time')
    df = pd.pivot_table(df, values='Value', index='Time', columns='Name', dropna=False)

    df[R3] = df[R3_FLEX] + df[R3_STD]
    df[AFRR] = df[R2_UP] - df[R2_DOWN] + df[IGCC_UP] - df[IGCC_DOWN]
    df[MFRR] = df[BIDS_UP] - df[BIDS_DOWN] + df[R3]

    return df


if __name__ == '__main__':
    df_imbalance = imbalance_dataframe(imbalance_raw_data(False))
