#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep  9 18:38:19 2018

@author: nicolasquintin
"""
import urllib.request
import json
import datetime
import re
import numpy as np
import pandas as pd

def ImbalanceService():
    """
    INPUT = /
    OUTPUT = LIST CONTAINING THE JSON OUTPUT OF ELIA'S IMBALANCE WEBSERVICE
    """
    
    with urllib.request.urlopen("https://publications.elia.be/Publications/Publications/InternetImbalance.v1.svc/GetImbalanceMeasuresByTime") as url:
        data = json.loads(url.read().decode())
        for m in data:
            TimestampUtc = re.split('\(|\)', m["Time"])[1][:10]
            date = datetime.datetime.fromtimestamp(int(TimestampUtc))
            m["Time"] = date
    return data

def ImbalanceDataPandas(data):
    """
    INPUT = RAW DATA WHICH IS THE RESULT OF THE IMBALANCESERVICE() FUNCTION
    OUTPUT = PANDAS MATRIX CONTAINING THE REARRANGED DATA
    """
    
    #DECLARE EMPTY NUMPY ARRAYS 
    NRV = np.empty(0)
    SI = np.empty(0)
    TIME = np.empty(0)
    R2UP = np.empty(0)
    R2DOWN = np.empty(0)
    BIDUP = np.empty(0)
    BIDDOWN = np.empty(0)
    R3FLEX = np.empty(0)
    R3STD = np.empty(0)
    IGCCUP = np.empty(0)
    IGCCDOWN = np.empty(0)

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