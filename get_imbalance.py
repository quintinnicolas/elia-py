"""
@author: nicolasquintin
"""
import urllib.request
import json
import re
import pandas as pd
import ssl
from utils_elia import adapt_for_timezone

URL_IMBALANCE = r"https://publications.elia.be/Publications/Publications/InternetImbalance.v1.svc/GetImbalanceMeasuresByTime"


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

    df['R3'] = df['R3Flex'] + df['R3Std']
    df['aFRR'] = df['R2Up'] - df['R2Down'] + df['IGCCUp'] - df['IGCCDown']
    df['mFRR'] = df['BidsUp'] - df['BidsDown'] + df['R3Flex'] + df['R3Std']

    return df


if __name__ == '__main__':
    df_imbalance = imbalance_dataframe(imbalance_raw_data(False))
