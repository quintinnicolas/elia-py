"""
Author: nicolasquintin
"""
import json
import re
import ssl
import urllib.request
import pandas as pd
import datetime as dt
from numpy import nan
from xml.etree import ElementTree
from elia import *


class EliaClient:
    DATE_FORMAT = "%Y-%m-%d"
    ssl._create_default_https_context = ssl._create_unverified_context

    def __init__(self,
                 dtime_start: dt.datetime,
                 dtime_end: dt.datetime):
        self.dtime_start = dtime_start
        self.dtime_end = dtime_end

    def get_forecast_solar(self) -> pd.DataFrame:
        """ returns the solar forecast from elia """
        url = URL_SOLAR % (self.dtime_start.strftime(self.DATE_FORMAT),  self.dtime_end.strftime(self.DATE_FORMAT))
        with urllib.request.urlopen(url, context=ssl.SSLContext()) as url:
            raw_data = url.read().decode("iso-8859-1")
        xml = ElementTree.fromstring(raw_data)
        df = self.__parse_xml_to_dataframe(xml)
        return df

    def get_forecast_wind(self) -> pd.DataFrame:
        """ returns the wind forecast published by elia """
        url = URL_WIND % (self.dtime_start.strftime(self.DATE_FORMAT),  self.dtime_end.strftime(self.DATE_FORMAT))
        with urllib.request.urlopen(url, context=ssl.SSLContext()) as url:
            raw_data = url.read().decode("iso-8859-1")
        xml = ElementTree.fromstring(raw_data)
        df = self.__parse_xml_to_dataframe(xml)
        return df

    def get_forecast_load(self) -> pd.DataFrame:
        """ returns the load forecast published by elia """
        url = URL_LOAD_1 % (self.dtime_start.strftime(self.DATE_FORMAT), self.dtime_end.strftime(self.DATE_FORMAT))
        df = pd.read_excel(url)
        df.index = pd.to_datetime(df.DateTime, dayfirst=True)
        df = df.tz_localize("Europe/Brussels").tz_convert("utc")
        return df

    @staticmethod
    def get_actual_imbalance_volume() -> pd.DataFrame:
        """ returns the latest imbalance measurements published by Elia"""
        with urllib.request.urlopen(URL_IMBALANCE, context=ssl.SSLContext()) as url:
            json_data = json.loads(url.read().decode())

        # The format of dtime is '/Date(1632802500000+0200)/'
        # However, this corresponds to epoch in utc timestamp (despite the +0200)!
        for item in json_data:
            timestamp_utc = int(re.split('\(|\)', item["Time"])[1][:10])
            dtime = UTC.localize(dt.datetime.utcfromtimestamp(timestamp_utc))
            item["Time"] = dtime  # replace item in soup

        df = pd.json_normalize(json_data, "Measurements", "Time")
        df = pd.pivot_table(df, values="Value", index="Time", columns="Name", dropna=False)
        df[R3] = df[R3_FLEX] + df[R3_STD]
        df[AFRR] = df[R2_UP] - df[R2_DOWN] + df[IGCC_UP] - df[IGCC_DOWN]
        df[MFRR] = df[BIDS_UP] - df[BIDS_DOWN] + df[R3]
        return df

    def get_actual_imbalance_prices_per_quarter_via_excel(self) -> pd.DataFrame:
        """ returns the imbalance prices on a 15min-basis published by Elia"""
        df = []
        for date in pd.date_range(self.dtime_start, self.dtime_end, freq="D"):
            df_price = pd.read_excel(URL_IMB_PRICE_EXCEL % date.strftime(self.DATE_FORMAT), header=1)
            df_price.index = pd.to_datetime(
                df_price.Date + " " + df_price.Quarter.str[0:5],
                dayfirst=True
            )
            df_price.tz_localize("Europe/Brussels").tz_convert("utc")
            df.append(df_price)
        df = pd.concat([df_price])
        return df

    def get_actual_imbalance_prices_per_quarter(self) -> pd.DataFrame:
        """ returns the imbalance prices on a 15min-basis published by Elia"""
        for date in pd.date_range(self.dtime_start, self.dtime_end, freq="D"):
            with urllib.request.urlopen(URL_IMB_PRICE_XML % date.strftime(self.DATE_FORMAT), context=ssl.SSLContext()) as url:
                price_data = url.read().decode("iso-8859-1")
            try:  # xml variable does already exist
                xml.append(ElementTree.fromstring(price_data))
            except NameError:  # xml variable does not exist yet
                xml = ElementTree.fromstring(price_data)

        # Retrieve columns
        dic_imbalance = {}
        for column in COLUMNS:
            elements = xml.findall(PREFIX_XML + 'ImbalanceNrvPrices/' + PREFIX_XML + 'ImbalanceNrvPrice/' + PREFIX_XML + column)
            dic_imbalance[column] = [float(elem.text) for elem in elements]

        # Retrieve index
        elements = xml.findall(PREFIX_XML + 'ImbalanceNrvPrices/' + PREFIX_XML + 'ImbalanceNrvPrice/' + PREFIX_XML + DATETIME)
        index = pd.to_datetime([elem.text for elem in elements])

        # Convert to dataframe
        df = pd.DataFrame(dic_imbalance, index=index)
        df.index.name = DATETIME
        df = df.tz_localize("Europe/Brussels").tz_convert("utc")

        # Make sure dataframe is not empty
        assert len(df) > 0
        return df.tz_convert(UTC)

    @staticmethod
    def get_actual_imbalance_prices_per_minute() -> pd.DataFrame:
        """ returns the imbalance prices on a 1min-basis published by Elia"""
        with urllib.request.urlopen(URL_IMB_PRICE_PER_MIN, context=ssl.SSLContext()) as url:
            json_data = url.read().decode("iso-8859-1")

        df = pd.read_json(json_data)
        df.index = pd.to_datetime(df.minute)
        columns_to_drop = [col for col in df.columns if col not in COLUMNS_PER_MIN]
        df.drop(columns_to_drop, axis=1, inplace=True)
        return df

    @staticmethod
    def __parse_xml_to_dataframe(xml: ElementTree.Element) -> pd.DataFrame:
        # Retrieve relevant elements in the soup
        if "WindForecasting" in str(xml):
            webservice = '{http://schemas.datacontract.org/2004/07/Elia.PublicationService.DomainInterface.WindForecasting.v2}'
            prefix = webservice + 'ForecastGraphItems/' + webservice + 'WindForecastingGraphItem/'
            real_time = xml.findall(prefix + webservice + 'Realtime')
            most_recent = xml.findall(prefix + webservice + 'MostRecentForecast')
            day_ahead = xml.findall(prefix + webservice + 'DayAheadForecast')
            dtimes = xml.findall(prefix + webservice + 'StartsOn/' + '{http://schemas.datacontract.org/2004/07/System}DateTime')

        elif "SolarForecasting" in str(xml):
            webservice = '{http://schemas.datacontract.org/2004/07/Elia.PublicationService.DomainInterface.SolarForecasting.v4}'
            prefix = webservice + 'SolarForecastingChartDataForZoneItems/' + webservice + 'SolarForecastingChartDataForZoneItem/'
            real_time = xml.findall(prefix + webservice + 'RealTime')
            most_recent = xml.findall(prefix + webservice + 'MostRecentForecast')
            day_ahead = xml.findall(prefix + webservice + 'DayAheadForecast')
            dtimes = xml.findall(prefix + webservice + 'StartsOn/' + '{http://schemas.datacontract.org/2004/07/System}DateTime')

        # List comprehension to format data
        real_time = [float(elem.text) if float(elem.text) != -50 else nan for elem in real_time]
        most_recent = [float(elem.text) if float(elem.text) != -50 else nan for elem in most_recent]
        day_ahead = [float(elem.text) if float(elem.text) != -50 else nan for elem in day_ahead]
        dtimes = pd.to_datetime([elem.text for elem in dtimes])

        # Build DataFrame
        data_dic = {
            "most_recent": most_recent,
            "day_ahead": day_ahead,
            "real_time": real_time,
        }
        df = pd.DataFrame(data_dic, index=dtimes)
        df.index.name = DATETIME
        return df
