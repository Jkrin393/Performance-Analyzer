#https://www.alphavantage.co/documentation/

import pandas as pd
import requests as re
from config import API_KEY

#attempt to pull the daily value over N time. For now hardcoded as 1 week
def get_security_data(symbol):
    url=f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={API_KEY}&outputsize=compact'

    response=re.get(url)
    data=response.json()

    #print(data)
    with open("data.txt", 'w') as outfile:
        print(data, file=outfile)

get_security_data('AAPL')