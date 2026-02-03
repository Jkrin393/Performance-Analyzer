#https://www.alphavantage.co/documentation/
#https://pandas.pydata.org/docs/user_guide/index.html
#https://docs.python.org/3/howto/argparse.html

import pandas as pd
import requests as re
from config import API_KEY
import json
import argparse

#attempt to pull the daily value over N time. default to one week
def get_security_data(symbol, days=7):
    url=f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={API_KEY}&outputsize=compact'

    response=re.get(url)
    data=response.json()

    #print(data)
    with open("data.txt", 'w') as outfile:
        print(json.dumps(data, indent=2),file=outfile)

    if 'Time Series (Daily)' not in data:
        print(f'error fetching data for {symbol}')
        return None
    
    meta_data=data.get("Meta Data", {})
    meta_symbol=meta_data.get("2. Symbol")
    meta_last_refreshed_date = meta_data.get("3. Last Refreshed")

    time_series_data=data['Time Series (Daily)']
    time_series_df=pd.DataFrame.from_dict(time_series_data, orient='index')
    time_series_df.index=pd.to_datetime(time_series_df.index) #sorts in order
    time_series_df=time_series_df.astype(float)

    time_series_df=time_series_df.reset_index()
    time_series_df=time_series_df.rename(columns={"index":"Date"})

    time_series_df=time_series_df.tail(days)

    with open("dataframedata.txt", 'w') as outfile:
        print(f"Security Symbol: {meta_symbol}", file=outfile)
        print(f"Date report was run: {meta_last_refreshed_date}", file=outfile)
        print(file=outfile)
        print(time_series_df.to_string(index=False, float_format="{:.2f}".format), file=outfile) #index is converted to string without argument to remove


    return time_series_df

    

#read symbol from cli
if __name__=="__main__":
    cli_parser=argparse.ArgumentParser(description="fetch n days data for given security")
    cli_parser.add_argument(
        "symbol",
        type=str,
        help="security ticker/symbol"
    )
    cli_parser.add_argument(
        "--days", #double dashes for optional arguments
        type=int,
        default=7,
        help="Number of days to show. Default=7"
    )

    cli_arguments=cli_parser.parse_args()

    filtered_security_dataframe=get_security_data(cli_arguments.symbol, cli_arguments.days)