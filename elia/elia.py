from __future__ import annotations
from typing import Any
from typing_extensions import deprecated

import json
import datetime as dt

import pandas as pd
import requests

from .decorators import split_along_time

DATETIME_FORMAT = "%Y-%m-%d %H:%S"


class EliaPandasClient:
    """Simple Python 3 client for the Elia Open Data API"""
    BASE_URL = r"https://opendata.elia.be/api/explore/v2.1/"
    ENDPOINT = r"/catalog/datasets/%s/exports/json"

    def __init__(self) -> None:
        pass

    def get_current_system_imbalance(
            self,
            **params: Any) -> pd.DataFrame:
        """This report contains data for the current hour and is refreshed every minute. Instantaneous system imbalance
        (and its components) and the area control error (ACE) in Elia’s control area. All published values are
        non-validated values and can only be used for information purposes. This dataset contains data from
        22/05/2024 (MARI local go-live) on."""
        dataset = "ods169"
        df = self._execute_query(dataset, params)
        df = self._process_results(df)
        return df

    def get_imbalance_prices_per_min(
            self,
            **params: Any) -> pd.DataFrame:
        """The 1min imbalance prices are published as fast as possible and give an indication for the final imbalance
        price of the ISP (imbalance settlement period which is 15min). This report contains data for the current hour
        and is refreshed every minute. Notice that in this report we only provide non-validated data. This dataset
        contains data from 22/05/2024 (MARI local go-live) on."""
        dataset = "ods161"
        df = self._execute_query(dataset, params)
        df = self._process_results(df)
        return df

    def get_solar_power_estimation_and_forecast(
            self,
            region: str | None = None,
            **params: Any) -> pd.DataFrame:
        """Intraday forecast, day-ahead and week-ahead forecast of photovoltaic power capacity on the Belgian grid.
        The values are updated every quarter-hour."""
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
        """Intraday forecast, day-ahead and week-ahead forecast of wind power capacity on the Belgian grid.
        The values are updated every quarter-hour."""
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
        """Measured and upscaled load on the Elia grid."""
        dataset = "ods003"
        where_filter = self._construct_where_filter(**locals())
        params.update({"where": where_filter})
        df = self._execute_query(dataset, params)
        df = self._process_results(df)
        return df
    
    def get_near_real_time_imbalance_prices_per_quarter_hour(
            self,
            **params: Any) -> pd.DataFrame:
        """Imbalance prices used for balance responsible parties (BRPs) settlement for every quarter hour. 
        This report contains data for the current day and is refreshed every quarter-hour.
        Notice that in this report we only provide non-validated data.
        This dataset contains data from 22/05/2024 (MARI local go-live) on."""
        dataset = "ods162"
        where_filter = self._construct_where_filter(**locals())
        params.update({"where": where_filter})
        df = self._execute_query(dataset, params)
        df = self._process_results(df)
        return df

    @deprecated("This method only returns data prior to 21/05/2024 (MARI go-live)")
    @split_along_time("5D")
    def get_historical_imbalance_prices_per_quarter_hour_before_mari(
            self,
            start: dt.datetime | dt.date | pd.Timestamp,
            end: dt.datetime | dt.date | pd.Timestamp,
            **params: Any) -> pd.DataFrame:
        """System imbalance prices applied if an imbalance is found between injections and offtakes in a balance
        responsible parties (BRPs) balance area. When imbalance prices are published on a quarter-hourly basis,
        the published prices have not yet been validated and can therefore only be used as an indication of the
        imbalance price.Only after the published prices have been validated can they be used for invoicing purposes.
        The records for month M are validated after the 15th of month M+1. Contains the historical data and is
        refreshed daily. This dataset contains data until 21/05/2024 (before MARI local go-live)."""
        dataset = "ods047"
        where_filter = self._construct_where_filter(**locals())
        params.update({"where": where_filter})
        df = self._execute_query(dataset, params)
        df = self._process_results(df)
        return df

    @split_along_time("5D")
    def get_historical_imbalance_prices_per_quarter_hour(
            self,
            start: dt.datetime | dt.date | pd.Timestamp,
            end: dt.datetime | dt.date | pd.Timestamp,
            **params: Any) -> pd.DataFrame:
        """Imbalance prices used for balancing responsible parties (BRPs)settlment. When imbalance prices are published
        on a quarter-hourly basis, the published prices have not yet been validated and can therefore only be used as
        an indication of the imbalance price. Only after the published prices have been validated can they be used for
        invoicing purposes. The records for month M are validated after the 15th of month M+1. Contains the historical
        data and is refreshed daily. This dataset contains data from 22/05/2024 (MARI local go-live) on."""
        dataset = "ods134"
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
        """Measured and upscaled photovoltaic power generation on the Belgian grid.Please note that the measured and
        forecast values are in MW, it is of the users responsibility to interpret the values as such."""
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
        """Measured and upscaled wind power generation on the Belgian grid.Please note that the measured and forecast
         values are in MW, it is of the users responsibility to interpret the values as such."""
        dataset = "ods031"
        where_filter = self._construct_where_filter(**locals())
        params.update({"where": where_filter})
        df = self._execute_query(dataset, params)
        df = self._process_results(df)
        return df

    @deprecated("This method only returns data prior to 21/05/2024 (ICAROS go-live)")
    @split_along_time("MS")
    def get_historical_power_generation_by_fuel_type_before_icaros(
            self,
            start: dt.datetime | dt.date | pd.Timestamp,
            end: dt.datetime | dt.date | pd.Timestamp,
            fuel: str | None = None,
            **params: Any) -> pd.DataFrame:
        """Energy generated by unit operated under a Contract for the Injection of Production Units (CIPUs) signed with
        Elia, aggregated by fuel type. This dataset contains data until 21/05/2024 (before ICAROS local go-live)."""
        dataset = "ods033"
        where_filter = self._construct_where_filter(**locals())
        params.update({"where": where_filter})
        df = self._execute_query(dataset, params)
        df = self._process_results(df)
        return df

    def get_system_imbalance_forecast_for_current_quarter_hour(
            self,
            limit: int = 100,
            **params: Any) -> pd.DataFrame:
        """This report contains a forecast of the average quarter-hourly system imbalance in the current quarter-hour
        as well as an estimated probability distribution of the average quarter-hourly system imbalance in the current
        quarter hour. The data reflects Elia's own forecasts of the system imbalance. It must be noted that these
        forecasts can have a significant error margin, are not binding for Elia and are therefore merely shared for
        informational purposes and that under no circumstances the publication or the use of this information imply a
        shift in responsibility or liability towards Elia."""
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
        """The report contains a forecast of the average quarter-hourly system imbalance in the next quarter hour as
         well as an estimated probability distribution of the average quarter-hourly system imbalance in the next
         quarter hour. The data reflects Elia's own forecasts of the system imbalance. It must be noted that these
         forecasts can have a significant error margin, are not binding for Elia and are therefore merely shared for
         informational purposes and that under no circumstances the publication or the use of this information imply
         a shift in responsibility or liability towards Elia."""
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
