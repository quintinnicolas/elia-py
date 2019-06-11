#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 14 19:44:29 2018

@author: nicolasquintin
"""
import ServiceWind as file2
import matplotlib.pyplot as plt
plt.switch_backend('agg')
from datetime import date
from datetime import timedelta
from datetime import datetime
import numpy as np

startdate = str(date.today() )
enddate = str(date.today() + timedelta(1))
root = file2.WindService(startdate, enddate)
WindData = file2.WindDataPandas(root)

fig = plt.figure(figsize=(8,4))
plt.plot(WindData.DAYAHEAD, 'r', label = 'DAY-AHEAD FORECAST')
plt.plot(WindData.MOSTRECENT, 'b', label = 'MOST RECENT FORECAST')
plt.plot(WindData.REALTIME, 'k', label = 'REAL TIME')
plt.ylabel('MW')
plt.legend()
plt.xlabel('TIME')
plt.title('Wind data ELIA from ' + startdate + ' to ' + enddate + ' in Belgium')
plt.grid(True)
plt.show()