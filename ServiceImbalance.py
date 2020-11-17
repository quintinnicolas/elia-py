#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep  9 18:38:19 2018

@author: nicolasquintin
"""
import urllib.request
import json
import re
import numpy as np
import pandas as pd

def ImbalanceService(utc = False):
    """
    INPUT = /
    OUTPUT = LIST CONTAINING THE JSON OUTPUT OF ELIA'S IMBALANCE WEBSERVICE
    """

    with urllib.request.urlopen("https://publications.elia.be/Publications/Publications/InternetImbalance.v1.svc/GetImbalanceMeasuresByTime") as url:
        data = json.loads(url.read().decode())
        for m in data:
            TimestampUtc = re.split('\(|\)', m["Time"])[1][:10]
            date = pd.Timestamp.utcfromtimestamp(int(TimestampUtc))
            if not(utc):
                m["Time"] = adapt_for_timezone(date)
            else:
                m["Time"] = date
    return data

def adapt_for_timezone(date,timezonefrom="utc",timezoneto="Europe/Brussels"):
    """

    Parameters
    ----------
    date : pandas timestamp object with implicit UTC timezone

    Returns
    -------
    date : pandas timestamp object with implicit belgian timezone

    """
    from pytz import timezone
    
    initial = timezone(timezonefrom)
    final = timezone(timezoneto)
    
    date = initial.localize(date)
    date = date.tz_convert(final).tz_localize(None)
    return date

def ImbalanceDataPandas(data):
    """
    INPUT = RAW DATA WHICH IS THE RESULT OF THE IMBALANCESERVICE() FUNCTION
    OUTPUT = PANDAS MATRIX CONTAINING THE REARRANGED DATA
    """
    
    #DECLARE EMPTY NUMPY ARRAYS 
    NRV = SI = TIME = R2UP = R2DOWN = BIDUP = BIDDOWN = \
    R3FLEX = R3STD = IGCCUP = IGCCDOWN = np.empty(0)
    
    #LOOP OVER THE DATA AND ARRANGE THEM INTO NUMPY ARRAY.
    #IF AN ERROR OCCURS, SIMPLY REPLACE THE MISSING DATA WITH NAN 
    for i in data:
        try:
            TIME = np.append(TIME,i["Time"])
        except:
            TIME = np.append(TIME,np.nan)
        try:
            SI = np.append(SI,float(i["Measurements"][0]["Value"]))
        except:
            SI = np.append(SI,np.nan)
        try:
            NRV = np.append(NRV,float(i["Measurements"][1]["Value"]))
        except:
            NRV = np.append(NRV,np.nan)        
        try:
            R2UP = np.append(R2UP,float(i["Measurements"][5]["Value"]))
        except:
            R2UP = np.append(R2UP,np.nan)
        try:
            R2DOWN = np.append(R2DOWN,float(-i["Measurements"][13]["Value"]))
        except:
            R2DOWN = np.append(R2DOWN,np.nan)
        try:
            BIDUP = np.append(BIDUP,float(i["Measurements"][6]["Value"]))
        except:
            BIDUP = np.append(BIDUP,np.nan)
        try:
            BIDDOWN = np.append(BIDDOWN,float(-i["Measurements"][14]["Value"]))
        except:
            BIDDOWN = np.append(BIDDOWN,np.nan)
        try:
            R3FLEX = np.append(R3FLEX,float(i["Measurements"][8]["Value"]))
        except:
            R3FLEX = np.append(R3FLEX,np.nan)
        try:
            R3STD = np.append(R3STD,float(i["Measurements"][7]["Value"]))
        except:
            R3STD = np.append(R3STD,np.nan)
        try:
            IGCCUP = np.append(IGCCUP,float(i["Measurements"][4]["Value"]))
        except:
            IGCCUP = np.append(IGCCUP,np.nan)
        try:
            IGCCDOWN = np.append(IGCCDOWN,float(-i["Measurements"][12]["Value"]))
        except:
            IGCCDOWN = np.append(IGCCDOWN,np.nan)

    #REARRANGE NUMPY DATA INTO A PANDAS DATAFRAME (=MATRIX)
    ImbalanceData = {'NRV':NRV,'SI':SI,'R2UP':R2UP,'R2DOWN':R2DOWN,'BIDUP':BIDUP,
                     'BIDDOWN':BIDDOWN,'R3FLEX':R3FLEX, 'R3STD':R3STD, 'IGCCUP':IGCCUP,
                     'IGCCDOWN':IGCCDOWN,
                     'R3':ReplaceNaNwithZeros(R3FLEX) + ReplaceNaNwithZeros(R3STD),
                     'aFRR':ReplaceNaNwithZeros(R2UP)+ReplaceNaNwithZeros(R2DOWN)+
                     ReplaceNaNwithZeros(IGCCDOWN)+ReplaceNaNwithZeros(IGCCUP),
                     'mFRR':ReplaceNaNwithZeros(BIDUP)+ReplaceNaNwithZeros(BIDDOWN)+
                     ReplaceNaNwithZeros(R3FLEX)+ReplaceNaNwithZeros(R3STD)}
    ImbalanceData = pd.DataFrame(ImbalanceData, index=TIME)

    return ImbalanceData

def ReplaceNaNwithZeros(nparray):
    nparray[np.isnan(nparray)] = 0
    return nparray