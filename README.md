# elia-py
Simple Python 3 client for the Elia Open Data API 🤖

For more information about the Elia Open Data Platform, please refer to 
[https://opendata.elia.be/](https://opendata.elia.be/).

### Installation
```shell
pip install elia-py
```

### Usage
```python
import datetime as dt
from elia import elia

connection = elia.EliaPandasClient()
start = dt.datetime(2024, 1, 1)
end = dt.datetime(2024, 1, 15)

df = connection.get_imbalance_prices_per_quarter_hour(start=start, end=end)
```
### Notes
This work has been inspired by a similar project `entsoe-py` available on 
[GitHub](https://github.com/EnergieID/entsoe-py).
