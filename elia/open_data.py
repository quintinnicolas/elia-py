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


DATASET_ID = "ods088"
ENDPOINT = rf"/catalog/datasets/{DATASET_ID}/records/"
params = {
    "dataset": [DATASET_ID],
    "limit": 10,
}

# Record_path is supposed to point to an array of objects
response = requests.get(BASE_URL + ENDPOINT, params=params)
json_data = json.loads(response.text)
df = pd.json_normalize(json_data, record_path=["records"])

# Keep only the necessary columns
cols = [col for col in df.columns if "record.fields." in col]
cols.append("record.timestamp")  # Add query time
df = df[cols]

# Rename columns
mapping_cols = {col: col.split(".")[-1] for col in cols}
df = df.rename(columns=mapping_cols)

# Handle datetimes!
df["datetime"] = pd.to_datetime(df["datetime"])
df["timestamp"] = pd.to_datetime(df["timestamp"])
df = df.set_index("datetime").sort_index()
