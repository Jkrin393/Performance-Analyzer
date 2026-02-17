#https://www.alphavantage.co/documentation/
#https://pandas.pydata.org/docs/user_guide/index.html
#https://docs.python.org/3/howto/argparse.html

import pandas as pd
import requests as re
from config import API_KEY
import time
from utils.file_writer import save_raw_data_payload

#pull the daily value over N time. default to one week
def get_security_data(symbol, days=7):
    url=f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={API_KEY}' #&outputsize=compact

    response=re.get(url)
    data=response.json()

    #print(data)
    #with open("output_files/data.txt", 'w') as outfile:
    #    print(json.dumps(data, indent=2),file=outfile)
    save_raw_data_payload(data)

    if 'Time Series (Daily)' not in data:
        print(f'error fetching data for {symbol}')
        return None
    
    meta_data=data.get("Meta Data", {})
    meta_last_refreshed_date = meta_data.get("3. Last Refreshed")

    time_series_data=data['Time Series (Daily)']
    time_series_df=pd.DataFrame.from_dict(time_series_data, orient='index')
    time_series_df.index=pd.to_datetime(time_series_df.index) #sorts in order
    time_series_df=time_series_df.astype(float)

    time_series_df=time_series_df.reset_index()
    time_series_df=time_series_df.rename(columns={"index":"Date"})
    time_series_df["Symbol"] = symbol
    time_series_df=time_series_df.tail(days)

    return time_series_df, meta_last_refreshed_date

def fetch_multiple_securities(symbols, days=7):
    data_by_symbol={}
    last_refreshed_dates={}

    for ticker in symbols:
        security_data=get_security_data(ticker,days)
        if security_data is None:
            continue
            
        current_dataframe, date_report_was_run=security_data
        data_by_symbol[ticker]=current_dataframe
        last_refreshed_dates[ticker]=date_report_was_run

        #Free tier of Alpha Vantage limits time before a second get request is allowed. 15 seconds seem to be enough to get the second request successfully
        time.sleep(15)

    if not data_by_symbol:
        return None, None
    

    return data_by_symbol, last_refreshed_dates


