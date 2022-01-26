import datetime as dt
import pytest
from elia import elia

start_1 = dt.datetime.today() - dt.timedelta(days=10)
end_1 = dt.datetime.today() - dt.timedelta(days=-1)

start_2 = dt.datetime.utcnow() - dt.timedelta(hours=12)
end_2 = dt.datetime.utcnow() + dt.timedelta(hours=12)


@pytest.fixture()
def connection() -> elia.EliaPandasClient:
    """Creates EliaClient object"""
    return elia.EliaPandasClient()


@pytest.mark.parametrize("start, end", [(start_1, end_1), (start_2, end_2)])
def test_historical_wind_power_estimation_and_forecast(connection, start, end):
    """Testing wind query"""
    df_test = connection.get_historical_wind_power_estimation_and_forecast(start=start, end=end)
    number_of_quarter_hours = (end-start).days * 24 * 4 + (end-start).seconds // 900
    print(df_test)
    assert(df_test.index.nunique() >= number_of_quarter_hours)


@pytest.mark.parametrize("start, end", [(start_1, end_1), (start_2, end_2)])
def test_historical_solar_power_estimation_and_forecast(connection, start, end):
    """Testing solar query"""
    df_test = connection.get_historical_solar_power_estimation_and_forecast(start=start, end=end)
    number_of_quarter_hours = (end-start).days * 24 * 4 + (end-start).seconds // 900
    print(df_test)
    assert(df_test.index.nunique() >= number_of_quarter_hours)


@pytest.mark.parametrize("start, end", [(start_1, end_1), (start_2, end_2)])
def test_load_on_elia_grid(connection, start, end):
    """Testing consumption query"""
    df_test = connection.get_load_on_elia_grid(start=start, end=end)
    number_of_quarter_hours = (end-start).days * 24 * 4 + (end-start).seconds // 900
    print(df_test)
    assert(df_test.index.nunique() >= number_of_quarter_hours)


@pytest.mark.parametrize("start, end", [(start_1, end_1), (start_2, end_2)])
def test_imbalance_prices_per_quarter(connection, start, end):
    """Testing imbalance price query"""
    df_test = connection.get_imbalance_prices_per_quarter_hour(start=start, end=end)
    number_of_quarter_hours = (end-start).days * 24 * 4 + (end-start).seconds // 900
    print(df_test)
    assert(df_test.index.nunique() >= number_of_quarter_hours)


def test_imbalance_prices_per_min(connection):
    """Testing imbalance price query"""
    df_test = connection.get_imbalance_prices_per_min()
    print(df_test)
    assert(df_test.index.nunique() >= 59)  # data per minute, only for the latest hour


def test_current_system_imbalance(connection):
    """Testing imbalance volume query"""
    df_test = connection.get_current_system_imbalance()
    print(df_test)
    assert(df_test.index.nunique() >= 59)  # data per minute, only for the latest hour
