"""
@author: nicolasquintin
"""
from __future__ import annotations
from typing import Any

import json
import datetime as dt

import pandas as pd
import requests

from .decorators import split_along_time

DATETIME_FORMAT = "%Y-%m-%d %H:%S"


class EliaPandasClient:
    """Simple Python 3 client for the Elia Open Data API"""
    BASE_URL = r"https://opendata.elia.be/api/v2"
    ENDPOINT = r"/catalog/datasets/%s/exports/json"

    def __init__(self) -> None:
        pass

    def get_current_system_imbalance(
            self,
            **params: Any) -> pd.DataFrame:
        """Returns the current system imbalance."""
        dataset = "ods088"
        df = self._execute_query(dataset, params)
        df = self._process_results(df)
        return df

    def get_imbalance_prices_per_min(
            self,
            **params: Any) -> pd.DataFrame:
        """Returns the current imbalance prices."""
        dataset = "ods077"
        df = self._execute_query(dataset, params)
        df = self._process_results(df)
        return df

    def get_solar_power_estimation_and_forecast(
            self,
            region: str | None = None,
            **params: Any) -> pd.DataFrame:
        """Returns solar power forecasts."""
        dataset = "ods087"
        where_filter = self._construct_where_filter(**locals())
        params.update({"where": where_filter})
        df = self._execute_query(dataset, params)
        df = self._process_results(df)
        return df

    def get_wind_power_estimation_and_forecast(
            self,
            region: str | None = None,
            **params: Any) -> pd.DataFrame:
        """Returns wind power forecasts."""
        dataset = "ods086"
        where_filter = self._construct_where_filter(**locals())
        params.update({"where": where_filter})
        df = self._execute_query(dataset, params)
        df = self._process_results(df)
        return df

    @split_along_time("5D")
    def get_load_on_elia_grid(
            self,
            start: dt.datetime | dt.date | pd.Timestamp,
            end: dt.datetime | dt.date | pd.Timestamp,
            **params: Any) -> pd.DataFrame:
        """Returns the electrical load in the ELIA power system"""
        dataset = "ods003"
        where_filter = self._construct_where_filter(**locals())
        params.update({"where": where_filter})
        df = self._execute_query(dataset, params)
        df = self._process_results(df)
        return df

    @split_along_time("5D")
    def get_imbalance_prices_per_quarter_hour(
            self,
            start: dt.datetime | dt.date | pd.Timestamp,
            end: dt.datetime | dt.date | pd.Timestamp,
            **params: Any) -> pd.DataFrame:
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
            start: dt.datetime | dt.date | pd.Timestamp,
            end: dt.datetime | dt.date | pd.Timestamp,
            region: str | None = None,
            **params: Any) -> pd.DataFrame:
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
            start: dt.datetime | dt.date | pd.Timestamp,
            end: dt.datetime | dt.date | pd.Timestamp,
            region: str | None = None,
            **params: Any) -> pd.DataFrame:
        """Returns the measured and upscaled wind power generation on the Belgian grid."""
        dataset = "ods031"
        where_filter = self._construct_where_filter(**locals())
        params.update({"where": where_filter})
        df = self._execute_query(dataset, params)
        df = self._process_results(df)
        return df

    @split_along_time("5D")
    def get_historical_power_generation_by_fuel_type(
            self,
            start: dt.datetime | dt.date | pd.Timestamp,
            end: dt.datetime | dt.date | pd.Timestamp,
            fuel: str | None = None,
            **params: Any) -> pd.DataFrame:
        """Returns the measured power generation on the Belgian grid by fuel type."""
        dataset = "ods033"
        where_filter = self._construct_where_filter(**locals())
        params.update({"where": where_filter})
        df = self._execute_query(dataset, params)
        df = self._process_results(df)
        return df

    @split_along_time("5M")
    def get_installed_capacity_by_fuel_type(
            self,
            start: dt.datetime | dt.date | pd.Timestamp,
            end: dt.datetime | dt.date | pd.Timestamp,
            fuel: str | None = None,
            **params: Any) -> pd.DataFrame:
        """Returns the actual installed power generation on the Belgian grid."""
        dataset = "ods035"
        where_filter = self._construct_where_filter(**locals())
        params.update({"where": where_filter})
        df = self._execute_query(dataset, params)
        df = self._process_results(df)
        return df

    def get_system_imbalance_forecast_for_current_quarter_hour(
            self,
            limit: int = 100,
            **params: Any) -> pd.DataFrame:
        """Returns the imbalance prices forecast for the current quarter-hour"""
        dataset = "ods136"
        where_filter = self._construct_where_filter(**locals())
        params.update({"where": where_filter, "limit": limit})
        df = self._execute_query(dataset, params)
        df = self._process_results(df, datetime_field="predictiontimeutc")
        return df

    def get_system_imbalance_forecast_for_next_quarter_hour(
            self,
            limit: int = 100,
            **params: Any) -> pd.DataFrame:
        """Returns the imbalance prices forecast for the next quarter-hour"""
        dataset = "ods147"
        where_filter = self._construct_where_filter(**locals())
        params.update({"where": where_filter, "limit": limit})
        df = self._execute_query(dataset, params)
        df = self._process_results(df, datetime_field="predictiontimeutc")
        return df

    def _execute_query(
            self,
            dataset: str,
            params: dict) -> pd.DataFrame:
        """Executes the query and returns the raw DataFrame"""
        response = requests.get(self.BASE_URL + self.ENDPOINT % dataset, params=params)
        json_data = json.loads(response.text)
        df = pd.json_normalize(json_data)
        return df

    @staticmethod
    def _construct_where_filter(
            **kwargs: Any) -> str:
        """Constructs the 'where' filter expression to be passed as parameter to the query"""
        start, end = kwargs.get('start'), kwargs.get('end')
        region = kwargs.get('region')
        fuel = kwargs.get('fuel')
        params = kwargs.get('params')
        datetime_field = kwargs.get('datetime_field', 'datetime')

        date_filter = f"{datetime_field} IN [date'{start.strftime(DATETIME_FORMAT)}'" \
                      f"..date'{end.strftime(DATETIME_FORMAT)}'[" if (start and end) else None
        region_filter = f"region = '{region}'" if region else None
        fuel_filter = f"fuel = '{fuel}'" if fuel else None
        params_filter = params.get('where') if params else None

        return "AND ".join(filter(None, [date_filter, region_filter, fuel_filter, params_filter]))

    @staticmethod
    def _process_results(
            df: pd.DataFrame,
            datetime_field: str = "datetime") -> pd.DataFrame:
        """Processes and cleans the DataFrame"""
        if not df.empty:
            df[datetime_field] = pd.to_datetime(df[datetime_field])
            df = df.set_index(datetime_field).sort_index()
        return df
