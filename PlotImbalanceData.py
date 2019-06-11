#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep  9 20:06:49 2018

@author: nicolasquintin
"""

import ServiceImbalance as file1
import matplotlib.pyplot as plt
#plt.switch_backend('agg')
import numpy as np

#CALL TO ELIA'S WEBSERVICE AND RETRIEVE JSON DATA IN A LIST  
data = file1.ImbalanceService()

#TRANSFORM RAW DATA INTO PANDAS STRUCTURE
ImbalanceData = file1.ImbalanceDataPandas(data)

#PLOT BAR CHART  
range_between_ticks = 5
plt_bar_index = range(len(ImbalanceData))
fig3 = plt.figure(figsize=(8,4))
plt.bar(plt_bar_index, ImbalanceData['aFRR'], width=0.8, label='aFRR', alpha = 0.3, bottom=ImbalanceData['mFRR'])
plt.bar(plt_bar_index, ImbalanceData['mFRR'], width=0.8, label='mFRR', alpha = 0.3)
plt.xticks(np.arange(0,len(ImbalanceData),range_between_ticks), ImbalanceData.index[::range_between_ticks].strftime("%H:%M"), rotation=-45)
plt.plot(plt_bar_index, ImbalanceData['NRV'], 'b', label = 'NRV')
plt.plot(plt_bar_index, ImbalanceData['SI'], 'r', label = 'SI')
plt.ylabel('MW')
plt.xlabel('TIME')
plt.title('Activated Reserves ELIA \n from ' + ImbalanceData.index[0].strftime("%c") + '\n until ' + ImbalanceData.index[-1].strftime("%c"))
plt.grid(True)
plt.legend()
plt.show()