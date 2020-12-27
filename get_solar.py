"""
@author: nicolasquintin
"""
import urllib.request
import ssl
import xml.etree.ElementTree as ElementTree

URL_SOLAR = 'https://publications.elia.be/Publications/publications/solarforecasting.v4.svc/GetChartDataForZoneXml?dateFrom=%s&dateTo=%s&sourceId=1'


def solar_forecast(start_date, end_date):
    with urllib.request.urlopen(URL_SOLAR % (start_date, end_date), context=ssl.SSLContext()) as url:
        solar_data = url.read().decode("iso-8859-1")
        xml = ElementTree.fromstring(solar_data)
        return xml
