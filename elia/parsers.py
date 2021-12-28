"""
Author: nicolasquintin
"""
from typing import List
from xml.etree import ElementTree

import pandas as pd
from numpy import nan
from pytz import timezone

UTC = timezone("utc")


def parse_renewable_xml(xml: ElementTree.Element) -> pd.DataFrame:
    """
    Retrieves relevant elements in the soup and parses the data into a DataFrame.
    The soup must come from either the Solar Forecast or the Wind Forecast query
    """
    if "WindForecasting" in str(xml):
        webservice = '{http://schemas.datacontract.org/2004/07/Elia.PublicationService.DomainInterface.WindForecasting.v2}'
        prefix = webservice + 'ForecastGraphItems/' + webservice + 'WindForecastingGraphItem/'
        real_time = xml.findall(prefix + webservice + 'Realtime')
        most_recent = xml.findall(prefix + webservice + 'MostRecentForecast')
        day_ahead = xml.findall(prefix + webservice + 'DayAheadForecast')
        dtimes = xml.findall(
            prefix + webservice + 'StartsOn/' + '{http://schemas.datacontract.org/2004/07/System}DateTime')

    elif "SolarForecasting" in str(xml):
        webservice = '{http://schemas.datacontract.org/2004/07/Elia.PublicationService.DomainInterface.SolarForecasting.v4}'
        prefix = webservice + 'SolarForecastingChartDataForZoneItems/' + webservice + 'SolarForecastingChartDataForZoneItem/'
        real_time = xml.findall(prefix + webservice + 'RealTime')
        most_recent = xml.findall(prefix + webservice + 'MostRecentForecast')
        day_ahead = xml.findall(prefix + webservice + 'DayAheadForecast')
        dtimes = xml.findall(
            prefix + webservice + 'StartsOn/' + '{http://schemas.datacontract.org/2004/07/System}DateTime')

    # List comprehension to format data where float(elem.text) != -50, since -50 holds for NaN
    real_time = [float(elem.text) if elem.text is not None else nan for elem in real_time]
    real_time = [value if value != -50 else nan for value in real_time]
    most_recent = [float(elem.text) if elem.text is not None else nan for elem in most_recent]
    most_recent = [value if value != -50 else nan for value in most_recent]
    day_ahead = [float(elem.text) if elem.text is not None else nan for elem in day_ahead]
    day_ahead = [value if value != -50 else nan for value in day_ahead]
    dtimes = pd.to_datetime([elem.text for elem in dtimes])

    # Build DataFrame
    data_dic = {
        "most_recent": most_recent,
        "day_ahead": day_ahead,
        "real_time": real_time,
    }
    df_parsed = pd.DataFrame(data_dic, index=dtimes)
    df_parsed.index.name = "DateTime"
    return df_parsed


def parse_imbalance_xmls(xmls: List[ElementTree.Element]) -> pd.DataFrame:
    """
    Retrieves relevant elements in the soup and parses the data into a DataFrame.
    The soup must come from the Imbalance query
    """

    # Retrieve columns
    dic_imbalance = {}
    web_service = r'{http://schemas.datacontract.org/2004/07/Elia.PublicationService.DomainInterface.ImbalanceNrvPrice.V1}'
    prefix = web_service + 'ImbalanceNrvPrices/' + web_service + 'ImbalanceNrvPrice/' + web_service
    for column in ["Alpha", "Beta", "MDP", "MIP", "NRV", "SI", "PNeg", "PPos"]:
        elements = []
        for xml in xmls:
            elements += xml.findall(prefix + column)  # Concatenate lists
        dic_imbalance[column] = [float(elem.text) for elem in elements]

    # Retrieve index
    elements = []
    for xml in xmls:
        elements += xml.findall(prefix + "DateTime")  # Concatenate lists
    index = pd.to_datetime([elem.text for elem in elements])

    # Convert to dataframe
    df_imb = pd.DataFrame(dic_imbalance, index=index)
    df_imb.index = df_imb.index.map(
        lambda x: x.astimezone(UTC))  # Fix for months with DST -> timezone needs to be changed row per row
    df_imb = df_imb.tz_convert("utc")
    df_imb.index.name = "DateTime"
    return df_imb
