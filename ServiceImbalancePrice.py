#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 26 16:38:25 2019

@author: nicolasquintin
"""

def ImbalancePriceService(date):
    import pandas as pd
    url = 'https://publications.elia.be/Publications/Publications/ImbalanceNrvPrice.v3.svc/GetImbalanceNrvPricesExcel?day=' + date
    ImbalancePrice = pd.read_excel(url, header = 1)
    ImbalancePrice.index = pd.to_datetime(ImbalancePrice.Date + " " + ImbalancePrice.Quarter.str[0:5], dayfirst=True)
    return ImbalancePrice