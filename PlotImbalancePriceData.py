#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 26 16:43:59 2019

@author: nicolasquintin
"""

import ServiceImbalancePrice as file5
import matplotlib.pyplot as plt
#plt.switch_backend('agg')
from datetime import date
import numpy as np

#RETRIEVE DATA FROM ELIA'S WEBSITE INTO A DATAFRAME
date_today = str(date.today())
PriceData = file5.ImbalancePriceService(date_today)

#PLOT BAR CHART  
range_between_ticks = 5
plt_bar_index = range(len(PriceData))

#BAR CHART ON PRIMARY Y-AXIS
fig, ax1 = plt.subplots(figsize=(8,4))
ax1.bar(plt_bar_index, PriceData['\nNRV\n(MW)'], width=0.8, label='NRV', alpha = 0.2)
ax1.bar(plt_bar_index, PriceData['SI\n(MW)'], width=0.8, label='SI', alpha = 0.2)
ax1.set_ylabel('[MW]')
ax1.legend(loc="upper left")
plt.xticks(np.arange(0,len(PriceData),range_between_ticks), PriceData.index[::range_between_ticks].strftime("%H:%M"), rotation=-45)
plt.xlabel("TIME")

#LINE CHART ON SECONDARY Y-AXIS
ax2 = ax1.twinx()
ax2.plot(plt_bar_index, PriceData['POS\n(€/MWh)'], 'g', label = 'POS')  
ax2.plot(plt_bar_index, PriceData['NEG\n(€/MWh)'], 'r', label = 'NEG')
ax2.legend
ax2.set_ylabel('[€/MWh]')

#FIGURE PARAMETERS
plt.title('Imbalance Volumes & Prices in Belgium \n on %s from %s to %s' %(PriceData.index[0].strftime("%D"),PriceData.index[0].strftime("%H:%M"), PriceData.index[-1].strftime("%H:%M")))
plt.grid(True)
plt.legend()
plt.show()