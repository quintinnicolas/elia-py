"""
@author: nicolasquintin
"""
import urllib.request
import ssl
import xml.etree.ElementTree as ElementTree

from elia import URL_SOLAR


def solar_forecast(start_date, end_date):
    with urllib.request.urlopen(URL_SOLAR % (start_date, end_date), context=ssl.SSLContext()) as url:
        solar_data = url.read().decode("iso-8859-1")
        xml = ElementTree.fromstring(solar_data)
        return xml
