#https://www.alphavantage.co/documentation/
#https://pandas.pydata.org/docs/user_guide/index.html
#https://docs.python.org/3/howto/argparse.html

import pandas as pd
import requests as re
from config import API_KEY
import json
import argparse
import time

#pull the daily value over N time. default to one week
def calculate_security_value_metrics(security_data_by_ticker):
    if not security_data_by_ticker:
        return None
    
    combined_dataframe_for_comparison=pd.concat(security_data_by_ticker,names=["symbol"])
    comparison_metrics={}#start price, end price,  %change, $change, %return $avg daily return, volatility, risk/reward measurement

    for ticker, security_data in security_data_by_ticker.items():
        security_data=security_data.sort_values("Date")

        start_price=security_data['4. close'].iloc[0]
        end_price=security_data['4. close'].iloc[-1]
        total_return_in_dollars=end_price-start_price
        total_return_pecentage=((end_price-start_price)/start_price)*100
        security_data['daily_change']=security_data['4. close'].pct_change()*100
        avg_daily_percentage_change=security_data['daily_change'].mean()
        volatility=security_data['daily_change'].std()
        sharpe_risk_to_reward=avg_daily_percentage_change/volatility

        comparison_metrics[ticker]={
            'Start Price':start_price,
            'End Price':end_price,
            'Total Return($)':total_return_in_dollars,
            'Total Return(%)':total_return_pecentage,
            'Average Daily Change(%)':avg_daily_percentage_change,
            'Volatility(std dev)':volatility,
            'Risk to Reward(Sharpe Ratio)':sharpe_risk_to_reward,

        }
    
    comparison_dataframe=pd.DataFrame(comparison_metrics)

    with open('combined_dataframe.txt', 'w') as outfile:
        print(comparison_dataframe.to_string(float_format="{:.2f}".format), file=outfile)

    return comparison_dataframe

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




#read symbols from cli
if __name__=="__main__":
    cli_parser=argparse.ArgumentParser(description="fetch n days data for given securities")
    cli_parser.add_argument(
        "symbols",
        nargs="+",
        help="security tickers/symbols seperated by a space"
    )
    cli_parser.add_argument(
        "--days", #double dashes for optional arguments
        type=int,
        default=7,
        help="Number of days to show. Default=7"
    )

    cli_arguments=cli_parser.parse_args()


    security_data, last_refresh_dates=fetch_multiple_securities(cli_arguments.symbols, cli_arguments.days)
    calculate_security_value_metrics(security_data)

    if security_data is not None:
        with open("dataframedata.txt", 'w') as outfile:
            for symbol in cli_arguments.symbols:
                current_dataframe=security_data.get(symbol)
                print(f"Security Symbol: {symbol}", file=outfile)
                print(f"Date report was run: {last_refresh_dates[symbol]} \n", file=outfile)
                print(current_dataframe.to_string(index=False, float_format="{:.2f}".format) , file=outfile) #index is converted to string without argument to remove
                print(file=outfile)