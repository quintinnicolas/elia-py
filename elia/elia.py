"""
Author: nicolasquintin
"""
import datetime as dt
import json

import pandas as pd
import requests

from decorators import split_in_chunks

DATE_FORMAT = "%Y-%m-%d"
DATETIME_FORMAT = "%Y-%m-%d %H:%S"

__version__ = "0.1.0"


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

    @split_in_chunks("24h")
    def get_imbalance_prices_per_quarter_hour(self, start: dt.datetime, end: dt.datetime, rows: int = 100, **params) -> pd.DataFrame:
        """Returns the imbalance prices per 15min"""
        dataset = "ods047"
        date_filter = f"datetime IN [date'{start.strftime(DATETIME_FORMAT)}'..date'{end.strftime(DATETIME_FORMAT)}'["
        params.update({"where": date_filter, "rows": rows})
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


if __name__ == "__main__":
    client = EliaPandasClient()
    start = dt.datetime(2022, 1, 1)
    end = dt.datetime(2022, 1, 15, 19)
    df = client.get_imbalance_prices_per_quarter_hour(start=start, end=end)
    print(df)
