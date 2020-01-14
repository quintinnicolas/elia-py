# -*- coding: utf-8 -*-
"""
Created on Wed Dec 11 13:17:35 2019

@author: nicolasquintin
"""
import matplotlib.pyplot as plt
from matplotlib import pyplot
from matplotlib import rcParams
rcParams['font.sans-serif'] = ['DejaVu Sans']
rcParams.update({'font.size': 11})
plt.switch_backend('agg')
from datetime import date
from datetime import timedelta
import numpy as np
#from pandas.plotting import register_matplotlib_converters
#register_matplotlib_converters()
    
def PlotImbalancePriceData():
    import ServiceImbalancePrice as file5
    
    #RETRIEVE DATA FROM ELIA'S WEBSITE INTO A DATAFRAME
    date_today = str(date.today())
    PriceData = file5.ImbalancePriceService(date_today)
    
    #PLOT BAR CHART  
    range_between_ticks = max(len(PriceData)//10,1)
    plt_bar_index = range(len(PriceData))
    x_loc = np.arange(0,len(PriceData),range_between_ticks)
    x_label = PriceData.index[::range_between_ticks].strftime("%H:%M")
    
    #BAR CHART ON PRIMARY Y-AXIS
    fig, ax1 = plt.subplots(figsize=(8,4))
    ax1.bar(plt_bar_index, PriceData['\nNRV\n(MW)'].values, width=0.8, label='NRV', alpha = 0.15)
    ax1.bar(plt_bar_index, PriceData['SI\n(MW)'].values, width=0.8, label='SI', alpha = 0.15)
    ax1.set_ylabel('[MW]')
    ax1.legend(loc="upper left")
    
    #LINE CHART ON SECONDARY Y-AXIS
    ax2 = ax1.twinx()  
    ax2.plot(plt_bar_index, PriceData['NEG\n(€/MWh)'].values, '#FE5F55', label = 'NEG', linewidth=2.5)
    ax2.plot(plt_bar_index, PriceData['POS\n(€/MWh)'].values, '#00D5AE', label = 'POS', linewidth=2.5)
    ax2.legend
    ax2.set_ylabel('[€/MWh]')
    
    #FIGURE PARAMETERS
    for ax in fig.axes:
        pyplot.sca(ax)
        plt.xticks(x_loc, x_label, rotation=-45)
        plt.xlabel("TIME")
    plt.title('Imbalance Volumes & Prices in Belgium \n on %s from %s to %s' %(PriceData.index[0].strftime("%Y-%m-%d"),PriceData.index[0].strftime("%H:%M"), PriceData.index[-1].strftime("%H:%M")))
    plt.grid(True)
    plt.legend()
    plt.savefig("DataPrice.svg",bbox_inches='tight')
    #plt.show()
    
def PlotImbalanceData():

    import ServiceImbalance as file1
    
    #CALL TO ELIA'S WEBSERVICE AND RETRIEVE JSON DATA IN A LIST  
    data = file1.ImbalanceService(UTC = False)
    
    #TRANSFORM RAW DATA INTO PANDAS STRUCTURE
    ImbalanceData = file1.ImbalanceDataPandas(data)
    
    #PLOT BAR CHART  
    range_between_ticks = max(len(ImbalanceData)//10,1)
    plt_bar_index = range(len(ImbalanceData))
    x_loc = np.arange(0,len(ImbalanceData),range_between_ticks)
    x_label = ImbalanceData.index[::range_between_ticks].strftime("%H:%M")
    
    fig = plt.figure(figsize=(8,4))
    plt.bar(plt_bar_index, ImbalanceData['aFRR'].values, width=0.8, label='aFRR', alpha = 0.15, bottom=ImbalanceData['mFRR'])
    plt.bar(plt_bar_index, ImbalanceData['mFRR'].values, width=0.8, label='mFRR', alpha = 0.15)
    plt.plot(plt_bar_index, ImbalanceData['NRV'].values, '#00D5AE', label = 'NRV', linewidth=2.5)
    plt.plot(plt_bar_index, ImbalanceData['SI'].values, '#FE5F55', label = 'SI' , linewidth=2.5)
    plt.ylabel('[MW]')
    plt.xticks(x_loc,x_label,rotation=-45)
    plt.xlabel('TIME')
    plt.title('Activated Reserves in Belgium by ELIA \n on %s from %s to %s' %(ImbalanceData.index[0].strftime("%Y-%m-%d"),ImbalanceData.index[0].strftime("%H:%M"), ImbalanceData.index[-1].strftime("%H:%M")))
    plt.grid(True)
    plt.legend()
    fig.savefig("DataImbalance.svg",bbox_inches='tight')
    #plt.show()

def PlotLoadData():   
    
    import ServiceLoad as file4
    
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
    fig.savefig("DataLoad.svg",  bbox_inches='tight')
    #plt.show()

def PlotSolarData():
    
    import ServiceSolar as file3
    
    startdate = str(date.today() )
    enddate = str(date.today() + timedelta(1))
    root = file3.SolarService(startdate, enddate)
    SolarData = file3.XMLtoPandas(root)
    x_loc = SolarData.index[0::12]
    x_label = x_loc.format(formatter=lambda x: x.strftime('%H:%M'))
        
    fig = plt.figure(figsize=(8,4))
    plt.plot(SolarData.DAYAHEAD, '#FE5F55', label = 'DAY-AHEAD FORECAST',linewidth=2.5)
    plt.plot(SolarData.MOSTRECENT, '#00D5AE', label = 'MOST RECENT FORECAST',linewidth=2.5)
    plt.plot(SolarData.REALTIME, 'k', label = 'REAL TIME',linewidth=2.5)
    plt.ylabel('[MW]')
    plt.xticks(x_loc,x_label,rotation=-45)
    plt.legend()
    plt.xlabel('TIME')
    plt.title('Solar production in Belgium | %s' %startdate)
    plt.grid(True)
    fig.savefig("DataSolar.svg",bbox_inches='tight')
    #plt.show()
    
def PlotWindData():
    
    import ServiceWind as file2
    import ServiceSolar as file3
    
    startdate = str(date.today() )
    enddate = str(date.today() + timedelta(1))
    root = file2.WindService(startdate, enddate)
    WindData = file3.XMLtoPandas(root)
    x_loc = WindData.index[0::12]
    x_label = x_loc.format(formatter=lambda x: x.strftime('%H:%M'))
    
    fig = plt.figure(figsize=(8,4))
    plt.plot(WindData.DAYAHEAD, '#FE5F55', label = 'DAY-AHEAD FORECAST',linewidth=2.5)
    plt.plot(WindData.MOSTRECENT, '#00D5AE', label = 'MOST RECENT FORECAST',linewidth=2.5)
    plt.plot(WindData.REALTIME, 'k', label = 'REAL TIME',linewidth=2.5)
    plt.ylabel('[MW]')
    plt.xticks(x_loc,x_label,rotation=-45)
    plt.legend()
    plt.xlabel('TIME')
    plt.title('Wind production in Belgium | %s' %(startdate))
    plt.grid(True)
    fig.savefig("DataWind.svg",bbox_inches='tight')
    #plt.show()
    
if __name__ == "__main__":
    PlotSolarData()
    PlotWindData()