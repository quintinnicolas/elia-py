#!/usr/bin/env python3
# -*- coding: iso-8859-1 -*-
"""
Created on Fri Oct 12 17:00:00 2018

@author: nicolasquintin
"""
import ServiceSolar as file3
import matplotlib.pyplot as plt
#plt.switch_backend('agg')
from datetime import date
from datetime import timedelta
from datetime import datetime
import numpy as np

startdate = str(date.today() )
enddate = str(date.today() + timedelta(1))
root = file3.SolarService(startdate, enddate)
SolarData = file3.SolarDataPandas(root) 
    
fig = plt.figure(figsize=(8,4))
plt.plot(SolarData.DAYAHEAD, 'r', label = 'DAY-AHEAD FORECAST')
plt.plot(SolarData.MOSTRECENT, 'b', label = 'MOST RECENT FORECAST')
plt.plot(SolarData.REALTIME, 'k', label = 'REAL TIME')
plt.ylabel('MW')
plt.legend()
plt.xlabel('TIME')
plt.title('Solar data ELIA from ' + startdate + ' to ' + enddate +' in Belgium')
plt.grid(True)
plt.show()