#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 23 17:26:59 2018

@author: nicolasquintin
"""

def LoadService(startdate,enddate):
    import pandas as pd
    url = 'https://publications.elia.be/Publications/Publications/STLForecasting.v1.svc/ExportSTLFForecastGraph?fromDate=' + startdate +'T23%3A00%3A00.000Z&toDate=' + enddate + 'T23%3A00%3A00.000Z'
    load = pd.read_excel(url)
    load.index = pd.to_datetime(load.DateTime, dayfirst=True)
    return load
