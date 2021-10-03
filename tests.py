import unittest
import datetime as dt
from elia.elia import EliaClient


class TestEliaClient(unittest.TestCase):
    end = dt.datetime.today()
    start = end - dt.timedelta(days=2)
    client = EliaClient(start, end)

    def test_forecast_wind(self):
        df = self.client.get_forecast_wind()
        print(df.tail())
        self.assertTrue(len(df) > 0)

    def test_forecast_solar(self):
        df = self.client.get_forecast_solar()
        print(df.tail())
        self.assertTrue(len(df) > 0)

    def test_forecast_load(self):
        df = self.client.get_forecast_load()
        print(df.tail())
        self.assertTrue(len(df) > 0)

    def test_actual_imbalance_volume(self):
        df = self.client.get_actual_imbalance_volume()
        print(df.tail())
        self.assertTrue(len(df) > 0)

    def test_actual_imbalance_price_per_quarter(self):
        df = self.client.get_actual_imbalance_prices_per_quarter()
        print(df.tail())
        self.assertTrue(len(df) > 0)

    def test_actual_imbalance_price_per_quarter_via_excel(self):
        df = self.client.get_actual_imbalance_prices_per_quarter_via_excel()
        print(df.tail())
        self.assertTrue(len(df) > 0)

    def test_actual_imbalance_price_per_minute(self):
        df = self.client.get_actual_imbalance_prices_per_minute()
        print(df.tail())
        self.assertTrue(len(df) > 0)


if __name__ == '__main__':
    unittest.main()
