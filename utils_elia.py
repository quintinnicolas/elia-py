"""
@author: nicolasquintin
"""

import numpy as np
import pandas as pd
from pytz import timezone


def xml_to_dataframe(xml):
    
    if "WindForecasting" in str(xml):
        webservice = '{http://schemas.datacontract.org/2004/07/Elia.PublicationService.DomainInterface.WindForecasting.v2}'
        realtimelist = xml.findall(webservice + 'ForecastGraphItems/' + webservice + 'WindForecastingGraphItem/' + webservice + 'Realtime')
        mostrecentlist = xml.findall(webservice + 'ForecastGraphItems/' + webservice + 'WindForecastingGraphItem/' + webservice + 'MostRecentForecast')
        dayaheadlist = xml.findall(webservice + 'ForecastGraphItems/' + webservice + 'WindForecastingGraphItem/' + webservice + 'DayAheadForecast')
        timelist = xml.findall(webservice + 'ForecastGraphItems/' + webservice + 'WindForecastingGraphItem/' + webservice + 'StartsOn/' + '{http://schemas.datacontract.org/2004/07/System}DateTime')
        
    elif "SolarForecasting" in str(xml):
        webservice = '{http://schemas.datacontract.org/2004/07/Elia.PublicationService.DomainInterface.SolarForecasting.v4}'
        realtimelist = xml.findall(webservice + 'SolarForecastingChartDataForZoneItems/' + webservice + 'SolarForecastingChartDataForZoneItem/' + webservice + 'RealTime')
        mostrecentlist = xml.findall(webservice + 'SolarForecastingChartDataForZoneItems/' + webservice + 'SolarForecastingChartDataForZoneItem/' + webservice + 'MostRecentForecast')
        dayaheadlist = xml.findall(webservice + 'SolarForecastingChartDataForZoneItems/' + webservice + 'SolarForecastingChartDataForZoneItem/' + webservice + 'DayAheadForecast')
        timelist = xml.findall(webservice + 'SolarForecastingChartDataForZoneItems/' + webservice + 'SolarForecastingChartDataForZoneItem/' + webservice + 'StartsOn/' + '{http://schemas.datacontract.org/2004/07/System}DateTime')
    
    index_dic = {"TIME": timelist}
    data_dic = {
        "MOSTRECENT": mostrecentlist,
        "DAYAHEAD": dayaheadlist,
        "REALTIME": realtimelist,
        }
    
    for key, values in index_dic.items():
        TIME = append_index(values)  
        
    df_final = pd.DataFrame()
    for key, values in data_dic.items():
        nparray = append_data(values)
        df = pd.DataFrame(nparray, index=TIME, columns=[key])
        df_final = pd.concat([df_final,df], axis=1)

    return df_final


def append_data(elements):
    np_array = np.empty(0)
    for element in elements: 
        try:
            if float(element.text) == -50:
                np_array = np.append(np_array, np.nan)
            else:
                np_array = np.append(np_array, float(element.text))
        except:
            np_array = np.append(np_array, np.nan)
    return np_array


def append_index(elements):
    np_array = np.empty(0)
    for element in elements:
        try:
            time = pd.to_datetime(element.text[:-1])
            time = adapt_for_timezone(time)
            np_array = np.append(np_array, time)
        except:
            np_array = np.append(np_array, np.nan)
    return np_array


def adapt_for_timezone(date, timezone_from="utc", timezone_to="Europe/Brussels"):

    initial = timezone(timezone_from)
    final = timezone(timezone_to)

    date = initial.localize(date)
    date = date.tz_convert(final).tz_localize(None)
    return date
