#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 23 18:00:09 2018

@author: nicolasquintin
"""
import ServiceLoad as file4
import matplotlib.pyplot as plt
from matplotlib import rcParams
rcParams['font.sans-serif'] = ['DejaVu Sans']
rcParams.update({'font.size': 11})
plt.switch_backend('agg')
from datetime import date
from datetime import timedelta

enddate = str(date.today() )
startdate = str(date.today() - timedelta(1))
LoadData = file4.LoadService(startdate,enddate)
x_loc = LoadData.index[0::12]
x_label = x_loc.format(formatter=lambda x: x.strftime('%H:%M'))

fig = plt.figure(figsize=(8,4))
plt.plot(LoadData['Day-ahead'], '#FE5F55', label = 'DAY-AHEAD FORECAST',linewidth=2.5)
plt.plot(LoadData['Most recent'], '#00D5AE', label = 'MOST RECENT FORECAST',linewidth=2.5)
plt.plot(LoadData['Total load'], 'k', label = 'REAL TIME',linewidth=2.5)
plt.ylabel('[MW]')
plt.xticks(x_loc,x_label,rotation=-45)
plt.legend()
plt.xlabel('TIME')
plt.title('Power consumption in Belgium | %s' %enddate)
plt.grid(True)
plt.savefig("DataLoad.svg",  bbox_inches='tight')
#plt.show()
