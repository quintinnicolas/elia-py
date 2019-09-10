# -*- coding: utf-8 -*-
"""
Created on Tue Sep 10 17:00:29 2019

@author: IHE378
"""

# Import libraries
import pandas as pd
import matplotlib.pyplot as plt
import requests
import urllib.request


# Set the URL you want to webscrape from
url = 'http://www.elia.be/en/suppliers/purchasing-categories/energy-purchases/Ancillary-services/Ancillary-Services-Volumes-Prices'

#Hands down the easiest way to parse a HTML table is to use pandas.read_html() - it accepts both URLs and HTML.
#Source: https://stackoverflow.com/questions/6325216/parse-html-table-to-python-list

tables = pd.read_html(url) # Returns list of all tables on page
#tables = pd.read_html("elia.html") # Returns list of all tables on page
RawData = tables[2] # Select table of interest

Data = RawData
Data.columns = Data.iloc[0,:]
Data = Data.drop([0], axis=0)
Data = Data.reset_index()
Data = Data.drop(['index'], axis=1)

R1 = Data
R1 = R1[R1['Reserve Type']=='R1']
R1 = R1[R1['Country']!='FCR Common Auction']
weeks = [x[1:3] for x in R1.loc[:,'Delivery Period']]
R1['Week'] = weeks
prices = [pd.to_numeric(x) for x in R1.loc[:,'Average Price[€/Mw/h]']]
R1['Average Price[€/Mw/h]'] = prices
R1_pivot = R1.pivot(index='Week', columns='Service Type', values='Average Price[€/Mw/h]')

#FIX UNITS
R1_pivot['Upward'] = R1_pivot['Upward']/10
R1_pivot['Downward'] = R1_pivot['Downward']/10
R1_pivot['Symmetric100'] = R1_pivot['Symmetric100']/100
R1_pivot['Symmetric200'] = R1_pivot['Symmetric200']/100

fig = plt.figure(figsize=(12,4))
plt.plot(R1_pivot)
plt.ylabel('Average Auction Price [€/MW/h]')
plt.legend(R1_pivot.columns)
plt.xlabel('Week of Year')
plt.title('Average Contracted Price for R1')
plt.grid(True)
plt.show()

