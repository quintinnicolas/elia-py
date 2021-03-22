"""
@author: nicolasquintin
"""
import urllib.request
import ssl
import xml.etree.ElementTree as ElementTree

from elia import URL_WIND


def wind_forecast(start_date, end_date):
    with urllib.request.urlopen(URL_WIND % (start_date, end_date), context=ssl.SSLContext()) as url:
        wind_data = url.read().decode("iso-8859-1")
        xml = ElementTree.fromstring(wind_data)
        return xml
