#!/usr/bin/env python3
# -*- coding: iso-8859-1 -*-
"""
Created on Mon Sep 10 20:45:01 2018

@author: nicolasquintin
"""
import urllib.request
import json
from datetime import date
from datetime import timedelta
from datetime import datetime
import re
import numpy as np
import pandas as pd

def SolarService(startdate,enddate):
    import urllib.request
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
    
    #DECLARE EMPTY NUMPY ARRAYS 
    TIME = np.empty(0)
    DAYAHEAD = np.empty(0)
    MOSTRECENT = np.empty(0)
    REALTIME = np.empty(0)
    
    webservice = '{http://schemas.datacontract.org/2004/07/Elia.PublicationService.DomainInterface.SolarForecasting.v4}'
    realtimelist = root.findall(webservice + 'SolarForecastingChartDataForZoneItems/' + webservice + 'SolarForecastingChartDataForZoneItem/' + webservice + 'RealTime')
    mostrecentlist = root.findall(webservice + 'SolarForecastingChartDataForZoneItems/' + webservice + 'SolarForecastingChartDataForZoneItem/' + webservice + 'MostRecentForecast')
    dayaheadlist = root.findall(webservice + 'SolarForecastingChartDataForZoneItems/' + webservice + 'SolarForecastingChartDataForZoneItem/' + webservice + 'DayAheadForecast')
    timelist = root.findall(webservice + 'SolarForecastingChartDataForZoneItems/' + webservice + 'SolarForecastingChartDataForZoneItem/' + webservice + 'StartsOn/' + '{http://schemas.datacontract.org/2004/07/System}DateTime')

    #IF AN ERROR OCCURS, SIMPLY REPLACE THE MISSING DATA WITH NAN 
    for elements in realtimelist:
        try:
            if float(elements.text) == -50:
                REALTIME = np.append(REALTIME,np.nan)
            else:
                REALTIME = np.append(REALTIME,float(elements.text))
        except:
            REALTIME = np.append(REALTIME,np.nan)
    for elements in mostrecentlist:
        try:
            MOSTRECENT = np.append(MOSTRECENT,float(elements.text))
        except:
            MOSTRECENT = np.append(MOSTRECENT,np.nan)
    for elements in dayaheadlist:
        try:
            DAYAHEAD = np.append(DAYAHEAD,float(elements.text))
        except:
            DAYAHEAD = np.append(DAYAHEAD,np.nan)
    for elements in timelist:
        try:
            TIME = np.append(TIME,datetime.strptime(elements.text[:-1],'%Y-%m-%dT%H:%M:%S'))
        except:
            TIME = np.append(TIME,np.nan)
            
    SolarData = {'DAYAHEAD':DAYAHEAD,
                'MOSTRECENT':MOSTRECENT,
                'REALTIME':REALTIME}
    SolarData = pd.DataFrame(SolarData, index=TIME)
    return SolarData