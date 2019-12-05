#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep  9 20:06:49 2018

@author: nicolasquintin
"""

import ServiceImbalance as file1
import matplotlib.pyplot as plt
from matplotlib import rcParams
rcParams['font.sans-serif'] = ['Open Sans']
rcParams.update({'font.size': 11})
plt.switch_backend('agg')
import numpy as np

#CALL TO ELIA'S WEBSERVICE AND RETRIEVE JSON DATA IN A LIST  
data = file1.ImbalanceService()

#TRANSFORM RAW DATA INTO PANDAS STRUCTURE
ImbalanceData = file1.ImbalanceDataPandas(data)

#PLOT BAR CHART  
range_between_ticks = 5
plt_bar_index = range(len(ImbalanceData))
fig3 = plt.figure(figsize=(8,4))
plt.bar(plt_bar_index, ImbalanceData['aFRR'], width=0.8, label='aFRR', alpha = 0.1, bottom=ImbalanceData['mFRR'])
plt.bar(plt_bar_index, ImbalanceData['mFRR'], width=0.8, label='mFRR', alpha = 0.1)
plt.xticks(np.arange(0,len(ImbalanceData),range_between_ticks), ImbalanceData.index[::range_between_ticks].strftime("%H:%M"), rotation=-45)
plt.plot(plt_bar_index, ImbalanceData['NRV'], '#00D5AE', label = 'NRV', linewidth=2.5)
plt.plot(plt_bar_index, ImbalanceData['SI'], '#FE5F55', label = 'SI' , linewidth=2.5)
plt.ylabel('[MW]')
plt.xlabel('TIME')
plt.title('Activated Reserves in Belgium by ELIA \n on %s from %s to %s' %(ImbalanceData.index[0].strftime("%D"),ImbalanceData.index[0].strftime("%H:%M"), ImbalanceData.index[-1].strftime("%H:%M")))
plt.grid(True)
plt.legend()
plt.savefig("DataImbalance.png",bbox_inches='tight')
#plt.show()