#!/usr/bin/env python3
# -*- coding: iso-8859-1 -*-
"""
Created on Fri Oct 12 17:00:00 2018

@author: nicolasquintin
"""
import ServiceSolar as file3
import matplotlib.pyplot as plt
from matplotlib import rcParams
rcParams['font.sans-serif'] = ['Open Sans']
rcParams.update({'font.size': 11})
plt.switch_backend('agg')
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
plt.plot(SolarData.DAYAHEAD, '#FE5F55', label = 'DAY-AHEAD FORECAST',linewidth=2.5)
plt.plot(SolarData.MOSTRECENT, '#00D5AE', label = 'MOST RECENT FORECAST',linewidth=2.5)
plt.plot(SolarData.REALTIME, 'k', label = 'REAL TIME',linewidth=2.5)
plt.ylabel('[MW]')
plt.xticks(x_labels,rotation=-45)
plt.legend()
plt.xlabel('TIME')
plt.title('Solar production in Belgium | %s' %startdate)
plt.grid(True)
plt.savefig("DataSolar.png",bbox_inches='tight')
#plt.show()
