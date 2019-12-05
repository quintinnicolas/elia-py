#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 14 19:44:29 2018

@author: nicolasquintin
"""
import ServiceWind as file2
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
root = file2.WindService(startdate, enddate)
WindData = file2.WindDataPandas(root)
WindData.index = WindData.index.format(formatter=lambda x: x.strftime('%H:%M'))
x_labels = WindData.index[0::12]

fig = plt.figure(figsize=(8,4))
plt.plot(WindData.DAYAHEAD, '#FE5F55', label = 'DAY-AHEAD FORECAST',linewidth=2.5)
plt.plot(WindData.MOSTRECENT, '#00D5AE', label = 'MOST RECENT FORECAST',linewidth=2.5)
plt.plot(WindData.REALTIME, 'k', label = 'REAL TIME',linewidth=2.5)
plt.ylabel('[MW]')
plt.xticks(x_labels,rotation=-45)
plt.legend()
plt.xlabel('TIME')
plt.title('Wind production in Belgium | %s' %(startdate))
plt.grid(True)
plt.savefig("DataWind.png",bbox_inches='tight')
#plt.show()