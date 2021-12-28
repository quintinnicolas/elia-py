# elia-py
Python 3 client for the Elia web services, the Belgian Transmission System Operator.
For more information about the web services, please refer to 
[this page](https://www.elia.be/en/customers/customer-tools-and-extranet/the-b2b-xml-service).

### Installation
```shell
pip install elia-py
```

### Usage
```python
import datetime as dt
from elia import elia

connection = elia.EliaPandasClient()
start = dt.datetime(2021,1,1)
end = dt.datetime(2021,1,5)

df = connection.get_forecast_solar(start, end)
```

