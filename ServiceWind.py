#!/usr/bin/env python3
# -*- coding: iso-8859-1 -*-
"""
Created on Mon Sep 10 20:45:01 2018

@author: nicolasquintin
"""
import urllib.request
import xml.etree.ElementTree as ET

def WindService(startdate,enddate):
    with urllib.request.urlopen('https://publications.elia.be/Publications/Publications/WindForecasting.v2.svc/GetForecastData?beginDate=' + startdate + '&endDate=' + enddate + '&isOffshore=&isEliaConnected') as url:
        winddata = url.read().decode("iso-8859-1")
        root = ET.fromstring(winddata)
        return root