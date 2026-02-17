import pandas as pd
import re

def clean_company_name(name:str) -> str:
    patterns_to_remove=[
        #r"\bCommon Stock\b",
        r"\bOrdinary Shares\b",
        r"\bAmerican Depositary Shares\b",
        r"\bADS\b",
        r"\bDepositary Shares\b",
        r"\bClass A\b",
        r"\bCommon Shares\b",
        r"\bOrdinary Share\b",
        r"\bClass A Common Shares\b",
        r"\bRights\b",
        r"\bUnits\b",
        r"\bCumulative Perpetual Preferred Stock\b",
        r"\bCumulative Perpetual Preferred Shares\b",
        r"\bSeries A Redeemable Preferred Stock\b",

    ]

    cleaned_name=name
    for current_pattern in patterns_to_remove:
        cleaned_name=re.sub(current_pattern,"",cleaned_name,flags=re.IGNORECASE)

    cleaned_name=clean_non_common_stock_text(cleaned_name)

    cleaned_name=re.sub(r"\s+", " ", cleaned_name).strip() #remove leftover white spaces

    return cleaned_name

def clean_non_common_stock_text(name: str) -> str:
    cleaned_name=name
    
    cleaned_name=re.sub(r"each representing.*", "", cleaned_name, flags=re.IGNORECASE)
    #cleaned_name=re.sub(r"series [A-Z]", "", cleaned_name, flags=re.IGNORECASE)
    #cleaned_name=re.sub(r"\s\d+(\.\d+)?%\s.*", "", cleaned_name)
    cleaned_name=re.sub(r"\s+", " ", cleaned_name).strip()
    
    return cleaned_name

def clean_raw_ticker_file(filepath='../data/nasdaq_screener.csv'):

    df=pd.read_csv(filepath)
    df_cleaned=df[["Symbol", "Name"]]
    
    cleaned_company_names=[]
    for company in df_cleaned["Name"]:
        cleaned_company_name=clean_company_name(company)
        cleaned_company_names.append(cleaned_company_name)

    df_cleaned["Name"]=cleaned_company_names
    df_cleaned.to_csv("../data/tickers.csv", index=False)
    print(f"cleaned file created and saved")

if __name__ == "__main__":
    clean_raw_ticker_file()