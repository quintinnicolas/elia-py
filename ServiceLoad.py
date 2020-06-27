#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 23 17:26:59 2018

@author: nicolasquintin
"""
import pandas as pd

def LoadService(startdate,enddate):
    import pandas as pd
    url = 'https://publications.elia.be/Publications/Publications/STLForecasting.v1.svc/ExportSTLFForecastGraph?fromDate=' + startdate +'T23%3A00%3A00.000Z&toDate=' + enddate + 'T23%3A00%3A00.000Z'
    load = pd.read_excel(url)
    load.index = pd.to_datetime(load.DateTime, dayfirst=True)
    return load

def LoadService2():
    url = "https://griddata.elia.be/eliabecontrols.prod/interface/fdn/download/datadownload/0b48be166289678d663e9ed2f3ced7d7"
    load = pd.read_csv(url,index_col=[0,1,2],skiprows=[0],sep=";")
    load = load.drop('Unnamed: 103', 1)
    
    index=load.index.names
    columns=load.columns
    load = pd.melt(load.reset_index(),id_vars=index,value_vars=columns)
    
    #Create datetime
    load['Hour'] = load.apply(lambda x:int(x['variable'].split(":")[0])%24,axis=1)
    load['Minute'] = load.apply(lambda x:int(x['variable'].split(":")[1][:2]),axis=1)
    load.rename(columns={"yyyy": "Year", "mm": "Month", "dd": "Day"}, inplace=True)
    time_columns = ["Year", "Month", "Day", "Hour", "Minute"]
    load.index = pd.to_datetime(load[time_columns])
    load.drop(time_columns+['variable'], axis=1, inplace=True)
    
    #Convert str values to float and remove 0 values (corresponding to unexisting timestamps)
    load = load[load['value']!='NOT VALID']
    load['value'] = load['value'].apply(lambda x:float(x.replace(",", ".")))
    load = load[load['value']>0]
    
    #DST's issue in csv: data go from 01:45 -> 02:00 -> 03:15 instead of 01:45 -> 03:00 -> 03:15
    load.rename(index={pd.to_datetime('2020-03-29 02:00:00'):pd.to_datetime('2020-03-29 03:00:00')},
                inplace=True)
    #Sort data and localize belgian timezone
    load = load.sort_index()
    load = load.tz_localize("Europe/Brussels")

    return load

