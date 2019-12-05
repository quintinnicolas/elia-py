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
SolarData.index = SolarData.index.format(formatter=lambda x: x.strftime('%H:%M'))
x_labels = SolarData.index[0::12]
    
fig = plt.figure(figsize=(8,4))
plt.plot(SolarData.DAYAHEAD, 'r', label = 'DAY-AHEAD FORECAST')
plt.plot(SolarData.MOSTRECENT, 'b', label = 'MOST RECENT FORECAST')
plt.plot(SolarData.REALTIME, 'k', label = 'REAL TIME')
plt.ylabel('[MW]')
plt.xticks(x_labels)
plt.legend()
plt.xlabel('TIME')
plt.title('Solar production in Belgium | %s' %startdate)
plt.grid(True)
plt.show()
