#!/usr/bin/env python3
# -*- coding: iso-8859-1 -*-
"""
Created on Mon Sep 10 20:45:01 2018

@author: nicolasquintin
"""
import urllib.request
import xml.etree.ElementTree as ET
import numpy as np
import pandas as pd
import ServiceImbalance

def SolarService(startdate,enddate):
    with urllib.request.urlopen('https://publications.elia.be/Publications/publications/solarforecasting.v4.svc/GetChartDataForZoneXml?dateFrom=' + startdate + '&dateTo=' + enddate + '&sourceId=1') as url:
        solardata = url.read().decode("iso-8859-1")
        root = ET.fromstring(solardata)
        return root
    
def XMLtoPandas(root):
    """
    INPUT = RAW DATA WHICH IS THE RESULT OF THE SOLARSERVICE() FUNCTION
    OUTPUT = PANDAS MATRIX CONTAINING THE REARRANGED DATA
    """    
    
    if "WindForecasting" in str(root):
        webservice = '{http://schemas.datacontract.org/2004/07/Elia.PublicationService.DomainInterface.WindForecasting.v2}'
        realtimelist = root.findall(webservice + 'ForecastGraphItems/' + webservice + 'WindForecastingGraphItem/' + webservice + 'Realtime')
        mostrecentlist = root.findall(webservice + 'ForecastGraphItems/' + webservice + 'WindForecastingGraphItem/' + webservice + 'MostRecentForecast')
        dayaheadlist = root.findall(webservice + 'ForecastGraphItems/' + webservice + 'WindForecastingGraphItem/' + webservice + 'DayAheadForecast')
        timelist = root.findall(webservice + 'ForecastGraphItems/' + webservice + 'WindForecastingGraphItem/'+ webservice + 'StartsOn/'+'{http://schemas.datacontract.org/2004/07/System}DateTime')
        
    elif "SolarForecasting" in str(root):
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
        
    df_final = pd.DataFrame()
    for key,values in data_dic.items():
        nparray = appenddata(values)
        df = pd.DataFrame(nparray,index=TIME,columns=[key])
        df_final = pd.concat([df_final,df],axis=1)

    return df_final

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
            timeindex = pd.to_datetime(elements.text[:-1])
            timeindex = ServiceImbalance.adapt_for_timezone(timeindex)
            np_array = np.append(np_array,timeindex)
        except:
            np_array = np.append(np_array,np.nan)
    return np_array



