#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 14 19:44:29 2018

@author: nicolasquintin
"""
import ServiceWind as file2
import matplotlib.pyplot as plt
#plt.switch_backend('agg')
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
plt.plot(WindData.DAYAHEAD, 'r', label = 'DAY-AHEAD FORECAST')
plt.plot(WindData.MOSTRECENT, 'b', label = 'MOST RECENT FORECAST')
plt.plot(WindData.REALTIME, 'k', label = 'REAL TIME')
plt.ylabel('[MW]')
plt.xticks(x_labels)
plt.legend()
plt.xlabel('TIME')
plt.title('Wind production in Belgium | %s' %(startdate))
plt.grid(True)
plt.show()