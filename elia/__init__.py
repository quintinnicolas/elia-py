"""
@author: nicolasquintin
"""

# Consumption constants
# Escape % symbol in url doubling the character (%%)
URL_LOAD_1 = "https://publications.elia.be/Publications/Publications/STLForecasting.v1.svc/ExportSTLFForecastGraph?fromDate=%sT23%%3A00%%3A00.000Z&toDate=%sT23%%3A00%%3A00.000Z"
URL_LOAD_2 = "https://griddata.elia.be/eliabecontrols.prod/interface/fdn/download/datadownload/0b48be166289678d663e9ed2f3ced7d7"

# Imbalance Volume constants
URL_IMBALANCE = "https://publications.elia.be/Publications/Publications/InternetImbalance.v1.svc/GetImbalanceMeasuresByTime"


# Imbalance Price constants
URL_IMB_PRICE_EXCEL = 'https://publications.elia.be/Publications/Publications/ImbalanceNrvPrice.v3.svc/GetImbalanceNrvPricesExcel?day=%s'
URL_IMB_PRICE_XML = "https://publications.elia.be/Publications/Publications/ImbalanceNrvPrice.v1.svc/GetImbalanceNrvPrices?day=%s"
PREFIX = r'{http://schemas.datacontract.org/2004/07/Elia.PublicationService.DomainInterface.ImbalanceNrvPrice.V1}'
ALPHA = "Alpha"
BETA = "Beta"
DATETIME = "DateTime"
MDP = "MDP"
MIP = "MIP"
NRV = "NRV"
P_NEG = "PNeg"
P_POS = "PPos"
SI = "SI"
COLUMNS = [ALPHA, BETA, MDP, MIP, NRV, SI, P_POS, P_NEG]

# Solar Data
URL_SOLAR = "https://publications.elia.be/Publications/publications/solarforecasting.v4.svc/GetChartDataForZoneXml?dateFrom=%s&dateTo=%s&sourceId=1"

# Wind Data
URL_WIND = "https://publications.elia.be/Publications/Publications/WindForecasting.v2.svc/GetForecastData?beginDate=%s&endDate=%s&isOffshore=&isEliaConnected="