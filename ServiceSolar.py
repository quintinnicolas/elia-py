#!/usr/bin/env python3
# -*- coding: iso-8859-1 -*-
"""
Created on Mon Sep 10 20:45:01 2018

@author: nicolasquintin
"""
import urllib.request
from datetime import datetime
import numpy as np
import pandas as pd

def SolarService(startdate,enddate):
    import xml.etree.ElementTree as ET
    with urllib.request.urlopen('https://publications.elia.be/Publications/publications/solarforecasting.v4.svc/GetChartDataForZoneXml?dateFrom=' + startdate + '&dateTo=' + enddate + '&sourceId=1') as url:
        solardata = url.read().decode("iso-8859-1")
        root = ET.fromstring(solardata)
        return root
    
def SolarDataPandas(root):
    """
    INPUT = RAW DATA WHICH IS THE RESULT OF THE SOLARSERVICE() FUNCTION
    OUTPUT = PANDAS MATRIX CONTAINING THE REARRANGED DATA
    """    
    
    webservice = '{http://schemas.datacontract.org/2004/07/Elia.PublicationService.DomainInterface.SolarForecasting.v4}'
    realtimelist = root.findall(webservice + 'SolarForecastingChartDataForZoneItems/' + webservice + 'SolarForecastingChartDataForZoneItem/' + webservice + 'RealTime')
    mostrecentlist = root.findall(webservice + 'SolarForecastingChartDataForZoneItems/' + webservice + 'SolarForecastingChartDataForZoneItem/' + webservice + 'MostRecentForecast')
    dayaheadlist = root.findall(webservice + 'SolarForecastingChartDataForZoneItems/' + webservice + 'SolarForecastingChartDataForZoneItem/' + webservice + 'DayAheadForecast')
    timelist = root.findall(webservice + 'SolarForecastingChartDataForZoneItems/' + webservice + 'SolarForecastingChartDataForZoneItem/' + webservice + 'StartsOn/' + '{http://schemas.datacontract.org/2004/07/System}DateTime')
    
    index_dic = {"TIME":timelist}
    data_dic = {
        "MOSTRECENT":mostrecentlist,
        "DAYAHEAD":dayaheadlist,
        "REALTIME":realtimelist,
        }
    
    for key,values in index_dic.items():
        TIME = appendindex(values)  
        
    df_solar = pd.DataFrame()
    for key,values in data_dic.items():
        nparray = appenddata(values)
        df = pd.DataFrame(nparray,index=TIME,columns=[key])
        df_solar = pd.concat([df_solar,df],axis=1)

    return df_solar

def appenddata(ET_list):
    np_array = np.empty(0)
    for elements in ET_list: 
        try:
            if float(elements.text) == -50:
                np_array = np.append(np_array,np.nan)
            else:
                np_array = np.append(np_array,float(elements.text))
        except:
            np_array = np.append(np_array,np.nan)
    return np_array

def appendindex(ET_list):
    np_array = np.empty(0)
    for elements in ET_list:
        try:
            np_array = np.append(np_array,datetime.strptime(elements.text[:-1],'%Y-%m-%dT%H:%M:%S'))
        except:
            np_array = np.append(np_array,np.nan)
    return np_array



