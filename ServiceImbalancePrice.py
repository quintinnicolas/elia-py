#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 26 16:38:25 2019

@author: nicolasquintin
"""
import pandas as pd
import ssl

def ImbalancePriceService(date):
    url = 'https://publications.elia.be/Publications/Publications/ImbalanceNrvPrice.v3.svc/GetImbalanceNrvPricesExcel?day=' + date
    ssl._create_default_https_context = ssl._create_unverified_context
    ImbalancePrice = pd.read_excel(url, header = 1)
    ImbalancePrice.index = pd.to_datetime(ImbalancePrice.Date + " " + ImbalancePrice.Quarter.str[0:5], dayfirst=True)
    return ImbalancePrice