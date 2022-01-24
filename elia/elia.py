"""
Author: nicolasquintin
"""
import datetime as dt
import json
import re
from xml.etree import ElementTree
from typing import Optional

import pandas as pd
import requests
from pytz import timezone

UTC = timezone("utc")
DATE_FORMAT = "%Y-%m-%d"

__version__ = "0.1.0"


class EliaPandasClient:
    BASE_URL = r"https://opendata.elia.be/api/v2"
    ENDPOINT = r"/catalog/datasets/%s/records/"

    def __init__(self):
        pass

    def get_current_system_imbalance(self, **params) -> pd.DataFrame:
        """Returns the current system imbalance data published by Elia"""

        params.update({"dataset": "ods088"})
        df = self._execute_query(params)
        df = self._process_results(df)
        return df

    def _execute_query(self, params: dict) -> pd.DataFrame:
        """Executes the query and return raw DataFrame"""

        response = requests.get(self.BASE_URL + self.ENDPOINT % params["dataset"], params=params)
        json_data = json.loads(response.text)
        df = pd.json_normalize(json_data, record_path=["records"])
        return df

    @staticmethod
    def _process_results(df) -> pd.DataFrame:
        """Processes and cleans the DataFrame"""

        # Keep only the necessary columns
        cols = [col for col in df.columns if "record.fields." in col]
        cols.append("record.timestamp")  # Add query time
        df = df[cols]

        # Rename columns
        mapping_cols = {col: col.split(".")[-1] for col in df.columns}
        df = df.rename(columns=mapping_cols)

        # Handle datetimes
        df["datetime"] = pd.to_datetime(df["datetime"])
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        df = df.set_index("datetime").sort_index()

        return df

    @staticmethod
    def get_forecast_solar(start: dt.datetime, end: dt.datetime, **kwargs) -> pd.DataFrame:
        """Returns the solar forecast from elia"""
        params = {
            "dateFrom": start.strftime(DATE_FORMAT),
            "dateTo": end.strftime(DATE_FORMAT),
            "sourceId": kwargs.get("source_id", 1),
        }
        response = requests.get("", params=params)
        xml = ElementTree.fromstring(response.text)
        # df_solar = parse_renewable_xml(xml)
        # return df_solar

    @staticmethod
    def get_forecast_wind(start: dt.datetime, end: dt.datetime, **kwargs) -> pd.DataFrame:
        """Returns the wind forecast published by elia"""
        params = {
            "beginDate": start.strftime(DATE_FORMAT),
            "endDate": end.strftime(DATE_FORMAT),
            "isOffshore": kwargs.get("is_offshore", 1),
            "isEliaConnected": kwargs.get("is_elia_connected", ""),
        }
        response = requests.get("", params=params)
        xml = ElementTree.fromstring(response.text)
        # df_wind = parse_renewable_xml(xml)
        # return df_wind

    @staticmethod
    def get_forecast_load(start: dt.datetime, end: dt.datetime) -> pd.DataFrame:
        """Returns the load forecast published by elia"""
        params = {
            "fromDate": start.isoformat(),
            "toDate": end.isoformat(),
        }
        url = requests.Request("GET", "", params=params).prepare()
        df_load = pd.read_excel(url.url)
        df_load.index = pd.to_datetime(df_load.DateTime, dayfirst=True)
        df_load = df_load.tz_localize("Europe/Brussels", ambiguous="infer").tz_convert("utc")
        return df_load

    @staticmethod
    def get_actual_imbalance_volume() -> pd.DataFrame:
        """Returns the latest imbalance measurements published by Elia"""
        response = requests.get("")
        json_data = json.loads(response.text)

        # The format of dtime is '/Date(1632802500000+0200)/'
        # However, this corresponds to epoch in utc timestamp (despite the +0200)!
        for item in json_data:
            timestamp_utc = int(re.split(r"\(|\)", item["Time"])[1][:10])
            dtime = UTC.localize(dt.datetime.utcfromtimestamp(timestamp_utc))
            item["Time"] = dtime  # replace item in soup

        # Load into DataFrame
        df_imb = pd.json_normalize(json_data, "Measurements", "Time")

        # A bit of post-processing
        df_imb = pd.pivot_table(df_imb, values="Value", index="Time", columns="Name", dropna=False)
        df_imb["R3"] = df_imb["R3Flex"] + df_imb["R3Std"]
        df_imb["aFRR"] = df_imb["R2Up"] - df_imb["R2Down"] + df_imb["IGCCUp"] - df_imb["IGCCDown"]
        df_imb["mFRR"] = df_imb["BidsUp"] - df_imb["BidsDown"] + df_imb["R3"]

        return df_imb

    @staticmethod
    def get_actual_imbalance_prices_per_quarter_via_excel(start: dt.datetime, end: dt.datetime) -> pd.DataFrame:
        """Returns the imbalance prices on a 15min-basis published by Elia"""
        df_imb = []
        for date in pd.date_range(start, end, freq="D"):
            params = {
                "day": date.strftime(DATE_FORMAT)
            }
            url = requests.Request("GET", "", params=params).prepare()
            df_price = pd.read_excel(url.url, header=1)

            # A bit of post-processing
            df_price.index = pd.to_datetime(
                df_price.Date + " " + df_price.Quarter.str[0:5],
                dayfirst=True
            )
            df_price = df_price.tz_localize("Europe/Brussels", ambiguous="infer").tz_convert("utc")
            df_imb.append(df_price)
        df_imb = pd.concat(df_imb)
        return df_imb

    @staticmethod
    def get_actual_imbalance_prices_per_quarter(start: dt.datetime, end: dt.datetime) -> pd.DataFrame:
        """Returns the imbalance prices on a 15min-basis published by Elia"""
        xmls = []  # List to store results of each day
        for date in pd.date_range(start, end, freq="D"):
            params = {
                "day": date.strftime(DATE_FORMAT)
            }
            response = requests.get("", params=params)
            xmls.append(ElementTree.fromstring(response.text))
        # df_imb = parse_imbalance_xmls(xmls)
        # assert len(df_imb) > 0  # Make sure dataframe is not empty
        # return df_imb

    @staticmethod
    def get_actual_imbalance_prices_per_minute() -> pd.DataFrame:
        """Returns the imbalance prices on a 1min-basis published by Elia"""
        response = requests.get("")
        json_data = json.loads(response.text)
        df_imb = pd.json_normalize(json_data)
        df_imb.index = pd.to_datetime(df_imb.minute)
        return df_imb


if __name__ == "__main__":
    client = EliaPandasClient()
    df = client.get_current_system_imbalance(rows=100)
    print(df)
