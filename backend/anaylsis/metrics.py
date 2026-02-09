import pandas as pd

def calculate_security_value_metrics(security_data_by_ticker):#### to do: add sortino ratio 
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
            'Sharpe Ratio':sharpe_risk_to_reward,

        }
    
    comparison_dataframe=pd.DataFrame(comparison_metrics)

   # with open('comparison_table.txt', 'w') as outfile:
   #     print(comparison_dataframe.to_string(float_format="{:.2f}".format), file=outfile)

    return comparison_dataframe

def suggest_best_security(comparison_dataframe):
    #consider adding CAGR, Max Drawdown, Sortino Ratio, beta comparison, dividend yield, annualized return w/ reinvestment
    
    sharpe_ratio_row=comparison_dataframe.loc['Sharpe Ratio']
    best_security_by_sharpe_ratio=sharpe_ratio_row.idxmax()
    best_security_metrics=comparison_dataframe[best_security_by_sharpe_ratio]

    return {
        "bestSecurity": best_security_by_sharpe_ratio,
        "bestMetrics": best_security_metrics.to_dict()
    }