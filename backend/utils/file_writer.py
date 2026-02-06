import json

def save_raw_data_payload(response_data, filepath="output_files/data.txt"):
    with open(filepath, 'w') as outfile:
        print(json.dumps(response_data, indent=2), file=outfile)

def save_dataframe_data(security_data, last_refresh_dates, symbols, filepath='output_files/dataframedata.txt'):
    with open(filepath, 'w') as outfile:
        for symbol in symbols:
            current_dataframe=security_data.get(symbol)
            if current_dataframe is not None:
                print(f"Security Symbol: {symbol}", file=outfile)
                print(f"Date report was run: {last_refresh_dates[symbol]} \n", file=outfile)
                print(current_dataframe.to_string(index=False, float_format="{:.2f}".format) , file=outfile) #index is converted to string without argument to remove
                print(file=outfile)

def save_comparison_report(comparison_dataframe, filepath='output_files/comparison_table.txt'):
    with open(filepath, 'w') as outfile:
        print(comparison_dataframe.to_string(float_format="{:.2f}".format), file=outfile)