"""
@author: nicolasquintin
"""
import pandas as pd
import ssl
import urllib.request
import xml.etree.ElementTree as ElementTree

from elia import URL_IMB_PRICE_EXCEL, URL_IMB_PRICE_XML, URL_IMB_PRICE_PER_MIN, PREFIX_XML, DATETIME, COLUMNS, \
    COLUMNS_PER_MIN


def imbalance_prices(date):
    ssl._create_default_https_context = ssl._create_unverified_context
    df_imbalance_prices = pd.read_excel(URL_IMB_PRICE_EXCEL % date, header=1)
    df_imbalance_prices.index = pd.to_datetime(df_imbalance_prices.Date + " " + df_imbalance_prices.Quarter.str[0:5],
                                               dayfirst=True)
    return df_imbalance_prices


def imbalance_prices_xml(date):
    with urllib.request.urlopen(URL_IMB_PRICE_XML % date, context=ssl.SSLContext()) as url:
        price_data = url.read().decode("iso-8859-1")
        xml = ElementTree.fromstring(price_data)

        # Retrieve columns
        dic_imbalance = {}
        for column in COLUMNS:
            elements = xml.findall(PREFIX_XML + 'ImbalanceNrvPrices/' + PREFIX_XML + 'ImbalanceNrvPrice/' + PREFIX_XML + column)
            dic_imbalance[column] = [float(elem.text) for elem in elements]

        # Retrieve index
        elements = xml.findall(PREFIX_XML + 'ImbalanceNrvPrices/' + PREFIX_XML + 'ImbalanceNrvPrice/' + PREFIX_XML + DATETIME)
        index = pd.to_datetime([elem.text for elem in elements])

        # Convert to dataframe
        df = pd.DataFrame(dic_imbalance, index=index)
        df.index.name = DATETIME

        # Make sure dataframe is not empty
        assert len(df)>0

        return df


def imbalance_prices_per_min():

    with urllib.request.urlopen(URL_IMB_PRICE_PER_MIN, context=ssl.SSLContext()) as url:
        json_data = url.read().decode("iso-8859-1")
        df = pd.read_json(json_data)
        df.index = pd.to_datetime(df.minute)

        columns_to_drop = [col for col in df.columns if col not in COLUMNS_PER_MIN]
        df.drop(columns_to_drop, axis=1, inplace=True)

        return df


if __name__ == '__main__':
    # df_test = imbalance_prices_xml("2020-03-20")
    df_test = imbalance_prices_per_min()
    print(df_test)
