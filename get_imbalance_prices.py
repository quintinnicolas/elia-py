"""
@author: nicolasquintin
"""
import pandas as pd
import ssl
import urllib.request
import xml.etree.ElementTree as ElementTree

URL_PRICE_EXCEL = 'https://publications.elia.be/Publications/Publications/ImbalanceNrvPrice.v3.svc/GetImbalanceNrvPricesExcel?day=%s'
URL_PRICE_XML = "https://publications.elia.be/Publications/Publications/ImbalanceNrvPrice.v1.svc/GetImbalanceNrvPrices?day=%s"


def imbalance_prices(date):
    ssl._create_default_https_context = ssl._create_unverified_context
    df_imbalance_prices = pd.read_excel(URL_PRICE_EXCEL % date, header=1)
    df_imbalance_prices.index = pd.to_datetime(df_imbalance_prices.Date + " " + df_imbalance_prices.Quarter.str[0:5],
                                               dayfirst=True)
    return df_imbalance_prices


def imbalance_prices_xml(date):
    with urllib.request.urlopen(URL_PRICE_XML % date, context=ssl.SSLContext()) as url:
        price_data = url.read().decode("iso-8859-1")
        xml = ElementTree.fromstring(price_data)

        prefix = r'{http://schemas.datacontract.org/2004/07/Elia.PublicationService.DomainInterface.ImbalanceNrvPrice.V1}'

        # Retrieve Positive Imbalances
        elements = xml.findall(prefix + 'ImbalanceNrvPrices/' + prefix + 'ImbalanceNrvPrice/' + prefix + 'PPos')
        positive_imbalance = [float(elem.text) for elem in elements]

        # Retrieve Negative Imbalances
        elements = xml.findall(prefix + 'ImbalanceNrvPrices/' + prefix + 'ImbalanceNrvPrice/' + prefix + 'PNeg')
        negative_imbalance = [float(elem.text) for elem in elements]

        # Retrieve Datetimes
        elements = xml.findall(prefix + 'ImbalanceNrvPrices/' + prefix + 'ImbalanceNrvPrice/' + prefix + 'DateTime')
        datetimes = pd.to_datetime([elem.text for elem in elements])

        # Convert to dataframe
        dic_columns = {"POS [EUR/MWh]": positive_imbalance,
                       "NEG [EUR/MWh]": negative_imbalance}
        df = pd.DataFrame(dic_columns, index=datetimes)

        return df
