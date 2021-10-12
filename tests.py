import pytest
import datetime as dt
from elia import elia


@pytest.fixture()
def elia_client() -> elia.EliaClient:
    """Creates EliaClient object"""
    end = dt.datetime.today()
    start = end - dt.timedelta(days=2)
    return elia.EliaClient(start, end)


def test_forecast_wind(elia_client):
    """Testing wind query"""
    df_test = elia_client.get_forecast_wind()
    print(df_test.tail())
    assert(len(df_test) >= 96)


def test_forecast_solar(elia_client):
    """Testing solar query"""
    df_test = elia_client.get_forecast_solar()
    print(df_test.tail())
    assert(len(df_test) >= 96)


def test_forecast_load(elia_client):
    """Testing consumption query"""
    df_test = elia_client.get_forecast_load()
    print(df_test.tail())
    assert(len(df_test) >= 96)


def test_actual_imbalance_volume(elia_client):
    """Testing imbalance volume query"""
    df_test = elia_client.get_actual_imbalance_volume()
    print(df_test.tail())
    assert(len(df_test) >= 59)  # data per minute, only for the latest hour


def test_actual_imbalance_price_per_quarter(elia_client):
    """Testing imbalance price query"""
    df_test = elia_client.get_actual_imbalance_prices_per_quarter()
    print(df_test.tail())
    assert(len(df_test) >= 96)


def test_actual_imbalance_price_per_quarter_via_excel(elia_client):
    """Testing imbalance price query"""
    df_test = elia_client.get_actual_imbalance_prices_per_quarter_via_excel()
    print(df_test.tail())
    assert(len(df_test) >= 96)


def test_actual_imbalance_price_per_minute(elia_client):
    """Testing imbalance price query"""
    df_test = elia_client.get_actual_imbalance_prices_per_minute()
    print(df_test.tail())
    assert(len(df_test) >= 59)  # data per minute, only for the latest hour
