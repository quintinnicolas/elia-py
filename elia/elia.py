"""
@author: nicolasquintin
"""
from __future__ import annotations

import json
import datetime as dt

import pandas as pd
import requests

from .decorators import split_along_time

DATETIME_FORMAT = "%Y-%m-%d %H:%S"
TODAY = dt.datetime.today()
YESTERDAY = dt.datetime.today() - dt.timedelta(days=1)


class EliaPandasClient:
    BASE_URL = r"https://opendata.elia.be/api/v2"
    ENDPOINT = r"/catalog/datasets/%s/exports/json"

    def __init__(self):
        pass

    def get_current_system_imbalance(self, **params) -> pd.DataFrame:
        """Returns the current system imbalance"""
        dataset = "ods088"
        df = self._execute_query(dataset, params)
        df = self._process_results(df)
        return df

    def get_imbalance_prices_per_min(self, **params) -> pd.DataFrame:
        """Returns the current imbalance prices"""
        dataset = "ods077"
        df = self._execute_query(dataset, params)
        df = self._process_results(df)
        return df

    def get_solar_power_estimation_and_forecast(
            self,
            region: str = None,
            **params) -> pd.DataFrame:
        """Returns the measured and upscaled photovoltaic power generation on the Belgian grid."""
        dataset = "ods087"
        where_filter = self._construct_where_filter(**locals())
        params.update({"where": where_filter})
        df = self._execute_query(dataset, params)
        df = self._process_results(df)
        return df

    def get_wind_power_estimation_and_forecast(
            self,
            region: str = None,
            **params) -> pd.DataFrame:
        """Returns the measured and upscaled wind power generation on the Belgian grid."""
        dataset = "ods086"
        where_filter = self._construct_where_filter(**locals())
        params.update({"where": where_filter})
        df = self._execute_query(dataset, params)
        df = self._process_results(df)
        return df

    @split_along_time("5D")
    def get_load_on_elia_grid(
            self,
            start: dt.datetime | pd.Timestamp = YESTERDAY,
            end: dt.datetime | pd.Timestamp = TODAY,
            **params) -> pd.DataFrame:
        """Returns the measured and upscaled photovoltaic power generation on the Belgian grid."""
        dataset = "ods003"
        where_filter = self._construct_where_filter(**locals())
        params.update({"where": where_filter})
        df = self._execute_query(dataset, params)
        df = self._process_results(df)
        return df

    @split_along_time("5D")
    def get_imbalance_prices_per_quarter_hour(
            self,
            start: dt.datetime | pd.Timestamp = YESTERDAY,
            end: dt.datetime | pd.Timestamp = TODAY,
            **params) -> pd.DataFrame:
        """Returns the imbalance prices per 15min"""
        dataset = "ods047"
        where_filter = self._construct_where_filter(**locals())
        params.update({"where": where_filter})
        df = self._execute_query(dataset, params)
        df = self._process_results(df)
        return df

    @split_along_time("5D")
    def get_historical_solar_power_estimation_and_forecast(
            self,
            start: dt.datetime | pd.Timestamp = YESTERDAY,
            end: dt.datetime | pd.Timestamp = TODAY,
            region: str = None,
            **params) -> pd.DataFrame:
        """Returns the measured and upscaled photovoltaic power generation on the Belgian grid."""
        dataset = "ods032"
        where_filter = self._construct_where_filter(**locals())
        params.update({"where": where_filter})
        df = self._execute_query(dataset, params)
        df = self._process_results(df)
        return df

    @split_along_time("5D")
    def get_historical_wind_power_estimation_and_forecast(
            self,
            start: dt.datetime | pd.Timestamp = YESTERDAY,
            end: dt.datetime | pd.Timestamp = TODAY,
            region: str = None,
            **params) -> pd.DataFrame:
        """Returns the measured and upscaled wind power generation on the Belgian grid."""
        dataset = "ods031"
        where_filter = self._construct_where_filter(**locals())
        params.update({"where": where_filter})
        df = self._execute_query(dataset, params)
        df = self._process_results(df)
        return df

    def _execute_query(self, dataset: str, params: dict) -> pd.DataFrame:
        """Executes the query and returns the raw DataFrame"""
        response = requests.get(self.BASE_URL + self.ENDPOINT % dataset, params=params)
        json_data = json.loads(response.text)
        df = pd.json_normalize(json_data)
        return df

    @staticmethod
    def _construct_where_filter(**kwargs) -> str:
        """Constructs the 'where' filter expression to be passed as parameter to the query"""
        start, end = kwargs.get('start'), kwargs.get('end')
        region = kwargs.get('region')
        params = kwargs.get('params')

        date_filter = f"datetime IN [date'{start.strftime(DATETIME_FORMAT)}'" \
                      f"..date'{end.strftime(DATETIME_FORMAT)}'[" if (start and end) else None
        region_filter = f"region = '{region}'" if region else None
        params_filter = params.get('where') if params else None

        return "AND ".join(filter(None, [date_filter, region_filter, params_filter]))

    @staticmethod
    def _process_results(df: pd.DataFrame) -> pd.DataFrame:
        """Processes and cleans the DataFrame"""
        df["datetime"] = pd.to_datetime(df["datetime"])
        df = df.set_index("datetime").sort_index()
        return df
