"""
@author: nicolasquintin
"""
import json
import logging
import datetime as dt

import pandas as pd
import requests

from constants import DATETIME_FORMAT
from decorators import split_along_time, split_in_chunks_if_too_long
from exceptions import TooManyRowsError, EmptyQueryError


class EliaPandasClient:
    BASE_URL = r"https://opendata.elia.be/api/v2"
    ENDPOINT = r"/catalog/datasets/%s/records/"

    def __init__(self):
        pass

    def get_current_system_imbalance(self, rows: int = 100, **params) -> pd.DataFrame:
        """Returns the current system imbalance"""
        dataset = "ods088"
        params.update({"rows": rows})
        df = self._execute_query(dataset, params)
        df = self._process_results(df)
        return df

    def get_imbalance_prices_per_min(self, rows: int = 100, **params) -> pd.DataFrame:
        """Returns the current imbalance prices"""
        dataset = "ods077"
        params.update({"rows": rows})
        df = self._execute_query(dataset, params)
        df = self._process_results(df)
        return df

    @split_along_time("24h")
    def get_imbalance_prices_per_quarter_hour(self, start: dt.datetime, end: dt.datetime, rows: int = 100, **params) -> pd.DataFrame:
        """Returns the imbalance prices per 15min"""
        dataset = "ods047"
        date_filter = f"datetime IN [date'{start.strftime(DATETIME_FORMAT)}'..date'{end.strftime(DATETIME_FORMAT)}'["
        params.update({"where": date_filter, "rows": rows})
        df = self._execute_query(dataset, params)
        df = self._process_results(df)
        return df

    @split_along_time("4h")
    @split_in_chunks_if_too_long(4)
    def get_solar_forecast(self, start: dt.datetime, end: dt.datetime, rows: int = 100, region: str = None, **params) -> pd.DataFrame:
        """Returns the measured and upscaled photovoltaic power generation on the Belgian grid."""
        dataset = "ods032"
        date_filter = f"datetime IN [date'{start.strftime(DATETIME_FORMAT)}'..date'{end.strftime(DATETIME_FORMAT)}'["
        region_filter = f"AND region = '{region}'" if region is not None else ""
        params.update({"where": date_filter + " " + region_filter, "rows": rows})
        df = self._execute_query(dataset, params)
        df = self._process_results(df)
        return df

    def _execute_query(self, dataset: str, params: dict) -> pd.DataFrame:
        """Executes the query and return raw DataFrame"""
        response = requests.get(self.BASE_URL + self.ENDPOINT % dataset, params=params)
        json_data = json.loads(response.text)
        df = pd.json_normalize(json_data, record_path=["records"])
        return df

    @staticmethod
    def _process_results(df: pd.DataFrame) -> pd.DataFrame:
        """Processes and cleans the DataFrame"""

        if len(df) >= 100:
            raise TooManyRowsError("The request reached the maximum number of rows imposed by the API."
                                   "Your query response will very likely contain some missing data. Please be careful!")

        if len(df) > 0:
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
    def __sanity_check(df: pd.DataFrame) -> None:
        """Checks if the dataframe looks healthy"""


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')
    client = EliaPandasClient()
    start_ = dt.datetime(2022, 1, 20)
    end_ = dt.datetime(2022, 1, 21, 19)
    df = client.get_solar_forecast(start=start_, end=end_, region="Brussels")
    print(df)
