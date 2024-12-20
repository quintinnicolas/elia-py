import datetime as dt
import pytest
from elia import elia

start_recent = dt.datetime.today() - dt.timedelta(days=10)
end_recent = dt.datetime.today() - dt.timedelta(days=2)

start_old, end_old = dt.datetime(2024, 5, 10, ), dt.datetime(2024, 5, 17)


@pytest.fixture()
def connection() -> elia.EliaPandasClient:
    """Creates EliaPandasClient object"""
    return elia.EliaPandasClient()


def test_wind_power_estimation_and_forecast(connection):
    """Testing wind query"""
    df_test = connection.get_wind_power_estimation_and_forecast()
    print(df_test)


def test_solar_power_estimation_and_forecast(connection):
    """Testing solar query"""
    df_test = connection.get_solar_power_estimation_and_forecast()
    print(df_test)


@pytest.mark.parametrize("start, end", [(start_recent, end_recent)])
def test_historical_wind_power_estimation_and_forecast(connection, start, end):
    """Testing wind query"""
    df_test = connection.get_historical_wind_power_estimation_and_forecast(start=start, end=end)
    number_of_quarter_hours = (end-start).days * 24 * 4 + (end-start).seconds // 900
    print(df_test)
    assert df_test.index.nunique() >= number_of_quarter_hours


@pytest.mark.parametrize("start, end", [(start_recent, end_recent)])
def test_historical_solar_power_estimation_and_forecast(connection, start, end):
    """Testing solar query"""
    df_test = connection.get_historical_solar_power_estimation_and_forecast(start=start, end=end)
    number_of_quarter_hours = (end-start).days * 24 * 4 + (end-start).seconds // 900
    print(df_test)
    assert df_test.index.nunique() >= number_of_quarter_hours


@pytest.mark.parametrize("start, end", [(start_old, end_old)])
def test_historical_power_generation_by_fuel_type(connection, start, end):
    """Testing generation query"""
    df_test = connection.get_historical_power_generation_by_fuel_type_before_icaros(start=start, end=end)
    number_of_quarter_hours = (end-start).days * 24 * 4 + (end-start).seconds // 900
    print(df_test)
    assert df_test.index.nunique() >= number_of_quarter_hours


@pytest.mark.parametrize("start, end", [(start_recent, end_recent)])
def test_load_on_elia_grid(connection, start, end):
    """Testing load query"""
    df_test = connection.get_load_on_elia_grid(start=start, end=end)
    number_of_quarter_hours = (end-start).days * 24 * 4 + (end-start).seconds // 900
    print(df_test)
    assert df_test.index.nunique() >= number_of_quarter_hours

def test_near_real_time_imbalance_prices_per_quarter(connection):
    """Testing imbalance price query, near real time"""
    df_test = connection.get_near_real_time_imbalance_prices_per_quarter_hour()
    assert not df_test.empty

@pytest.mark.parametrize("start, end", [(start_recent, end_recent)])
def test_imbalance_prices_per_quarter(connection, start, end):
    """Testing imbalance price query"""
    df_test = connection.get_historical_imbalance_prices_per_quarter_hour(start=start, end=end)
    number_of_quarter_hours = (end-start).days * 24 * 4
    print(df_test)
    assert df_test.index.nunique() >= number_of_quarter_hours


@pytest.mark.parametrize("start, end", [(start_old, end_old)])
def test_old_imbalance_prices_per_quarter(connection, start, end):
    """Testing imbalance price query"""
    df_test = connection.get_historical_imbalance_prices_per_quarter_hour_before_mari(start=start, end=end)
    number_of_quarter_hours = (end-start).days * 24 * 4
    print(df_test)
    assert df_test.index.nunique() >= number_of_quarter_hours


def test_imbalance_prices_per_min(connection):
    """Testing imbalance price query"""
    df_test = connection.get_imbalance_prices_per_min()
    print(df_test)
    assert df_test.index.nunique() >= 59  # data per minute, only for the latest hour


def test_current_system_imbalance(connection):
    """Testing imbalance volume query"""
    df_test = connection.get_current_system_imbalance()
    print(df_test)
    assert df_test.index.nunique() >= 59  # data per minute, only for the latest hour


def test_system_imbalance_forecast_for_current_quarter_hour(connection):
    """Testing imbalance forecast query"""
    df_test = connection.get_system_imbalance_forecast_for_current_quarter_hour(limit=10)
    print(df_test)
    assert df_test.index.nunique() == 10


def test_system_imbalance_forecast_for_next_quarter_hour(connection):
    """Testing imbalance forecast query"""
    df_test = connection.get_system_imbalance_forecast_for_next_quarter_hour(limit=10)
    print(df_test)
    assert df_test.index.nunique() == 10
