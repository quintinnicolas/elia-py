#!/usr/bin/env python3
# -*- coding: iso-8859-1 -*-
"""
Created on Mon Sep 10 20:45:01 2018

@author: nicolasquintin
"""
import numpy as np
import pandas as pd
from datetime import datetime

def WindService(startdate,enddate):
    import urllib.request
    import xml.etree.ElementTree as ET
    with urllib.request.urlopen('https://publications.elia.be/Publications/Publications/WindForecasting.v2.svc/GetForecastData?beginDate=' + startdate + '&endDate=' + enddate + '&isOffshore=&isEliaConnected') as url:
        winddata = url.read().decode("iso-8859-1")
        root = ET.fromstring(winddata)
        return root
    
def WindDataPandas(root):
    """
    INPUT = RAW DATA WHICH IS THE RESULT OF THE WINDSERVICE() FUNCTION
    OUTPUT = PANDAS MATRIX CONTAINING THE REARRANGED DATA
    """
    
    #DECLARE EMPTY NUMPY ARRAYS 
    TIME = np.empty(0)
    DAYAHEAD = np.empty(0)
    MOSTRECENT = np.empty(0)
    REALTIME = np.empty(0)
    
    #DECLARE THE ROOT XML STRUCTURE
    webservice = '{http://schemas.datacontract.org/2004/07/Elia.PublicationService.DomainInterface.WindForecasting.v2}'
    realtimelist = root.findall(webservice + 'ForecastGraphItems/' + webservice + 'WindForecastingGraphItem/' + webservice + 'Realtime')
    mostrecentlist = root.findall(webservice + 'ForecastGraphItems/' + webservice + 'WindForecastingGraphItem/' + webservice + 'MostRecentForecast')
    dayaheadlist = root.findall(webservice + 'ForecastGraphItems/' + webservice + 'WindForecastingGraphItem/' + webservice + 'DayAheadForecast')
    timelist = root.findall(webservice + 'ForecastGraphItems/' + webservice + 'WindForecastingGraphItem/'+ webservice + 'StartsOn/'+'{http://schemas.datacontract.org/2004/07/System}DateTime')
    
    #LOOP OVER THE DATA AND ARRANGE THEM INTO NUMPY ARRAY.
    #IF AN ERROR OCCURS, SIMPLY REPLACE THE MISSING DATA WITH NAN 
    for elements in realtimelist:
        try:
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
            
    WindData = {'DAYAHEAD':DAYAHEAD,
                'MOSTRECENT':MOSTRECENT,
                'REALTIME':REALTIME}
    WindData = pd.DataFrame(WindData, index=TIME)
    return WindData