"""
@author: nicolasquintin
@source: https://towardsdatascience.com/all-pandas-json-normalize-you-should-know-for-flattening-json-13eae1dfb7dd !!!
"""

import requests
import json
import pandas as pd

BASE_URL = r"https://opendata.elia.be/api/v2"
ENDPOINT = r"/catalog/datasets"

response = requests.get(BASE_URL + ENDPOINT)
json_data = json.loads(response.text)
df = pd.json_normalize(json_data, record_path=["datasets"])
df = pd.json_normalize(json_data, record_path=["datasets"], max_level=1)
print(df.info())


params = {
    "dataset": ["ods088"],
    "rows": 10,
    "start": 0,
    "facet": ["datetime", "resolutioncode"],
    "format": "json",
    "timezone": "UTC"
}

response = requests.get(BASE_URL + ENDPOINT)