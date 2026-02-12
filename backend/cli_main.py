import argparse
from api.alpha_vantage import fetch_multiple_securities
from backend.analysis.metrics import calculate_security_value_metrics, suggest_best_security
from utils.file_writer import save_dataframe_data, save_comparison_report

def main():
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

    #Alpha vantage free tier limnits to five securities
    if len(cli_arguments.symbols)>5:
        print("Maximum 5 symbols allowed")
        return

    security_data, last_refresh_dates=fetch_multiple_securities(cli_arguments.symbols, cli_arguments.days)
    if security_data is None:
        print("Error fetching security data")
        return
    print("Success fetching data")

    comparison_dataframe = calculate_security_value_metrics(security_data)
   # best_security, best_security_metrics = suggest_best_security(comparison_dataframe)
    best_result=suggest_best_security(comparison_dataframe)
    save_comparison_report(comparison_dataframe)
    save_dataframe_data(security_data,last_refresh_dates,cli_arguments.symbols)
    
    print(f"Best security based on Sharpe ratio: {best_result['bestSecurity']}")
    for metric, value in best_result['bestMetrics'].items():
        print(f" {metric}: {value:.2f}")

if __name__ == "__main__":
    main()