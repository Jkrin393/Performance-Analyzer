#https://fastapi.tiangolo.com/#interactive-api-docs
#https://fastapi.tiangolo.com/python-types/#union

from fastapi import FastAPI
from typing import List
from pydantic import BaseModel
from alphaApi.alpha_vantage import fetch_multiple_securities
from analysis.metrics import calculate_security_value_metrics, suggest_best_security
from fastapi.middleware.cors import CORSMiddleware
from utils.ticker_lookup import search_ticker
from database import Ticker, SessionLocal


app = FastAPI(
    title="Security Analyzer API",
    description="Compare securities and analyze performance metrics",
    version="1.0.0"
)
origins=[
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,        #domains
    allow_methods=["*"],          #all methods (GET, POST)
    allow_headers=["*"],          #all headers
)
class AnalysisRequest(BaseModel):
    symbols: List[str]
    days:int=7 #default to 7 days for now

@app.get("/")
def read_root():
    return {"message":"Success! the API is running!"}

@app.get("/health")
def health_check():
    return{"status":"healthy"}

@app.post("/api/analyze")
def analyze_securities(request: AnalysisRequest):
    if len(request.symbols)==0 or len(request.symbols)>5:
        return {"error":"please enter between 1 and 5 symbols"}
    
    symbols=request.symbols
    security_data,last_refresh_dates=fetch_multiple_securities(symbols,request.days)
    
    if security_data is None:
        return {"error: ": "couldnt fetch security data"}
    
    comparison_dataframe=calculate_security_value_metrics(security_data)

    best_result=suggest_best_security(comparison_dataframe)

    return {
        "comparisonTable":comparison_dataframe.to_dict(),
        "bestSecurity":best_result["bestSecurity"],
        "bestMetrics":best_result["bestMetrics"],
        "lastRefreshed":last_refresh_dates,
    }

    """best_security,best_metrics=suggest_best_security(comparison_dataframe)

    return {
        "comparison table":comparison_dataframe.to_dict(),
        "best security":best_security,
        "best_security's metrics":best_metrics,
        "date report was run":last_refresh_dates,
    }"""

#fake endpoint to prevent using up all free API requests
@app.post("/api/fakeanalyze")
def mock_analyze_securities(request: AnalysisRequest):
    
    import pandas as pd

    mock_comparison_data = {
        "AAPL": {
            "Start Price": 150.23,
            "End Price": 155.67,
            "Total Return($)": 5.44,
            "Total Return(%)": 3.62,
            "Average Daily Change(%)": 0.52,
            "Volatility(std dev)": 1.23,
            "Sharpe Ratio": 0.42
        },
        "NVDA": {
            "Start Price": 380.45,
            "End Price": 390.20,
            "Total Return($)": 9.75,
            "Total Return(%)": 2.56,
            "Average Daily Change(%)": 0.37,
            "Volatility(std dev)": 1.10,
            "Sharpe Ratio": 0.34
        },
        "GOOG": {
            "Start Price": 142.18,
            "End Price": 148.90,
            "Total Return($)": 6.72,
            "Total Return(%)": 4.73,
            "Average Daily Change(%)": 0.68,
            "Volatility(std dev)": 1.45,
            "Sharpe Ratio": 0.47
        }
    }
    
    comparison_dataframe = pd.DataFrame(mock_comparison_data)
    best_result = suggest_best_security(comparison_dataframe)
    
    last_refresh_dates = {
        "AAPL": "2024-02-06",
        "NVDA": "2024-02-06",
        "GOOGL": "2024-02-06"
    }
    
    return {
        "comparisonTable": comparison_dataframe.to_dict(),
        "bestSecurity": best_result["bestSecurity"],
        "bestMetrics": best_result["bestMetrics"],
        "lastRefreshed": last_refresh_dates,
    }

class TickerSearchRequest(BaseModel):
    query: str

@app.post("/api/search-ticker")
def search_ticker_endpoint(request: TickerSearchRequest):
    if not request.query or len(request.query) < 2:
        return {"results": []}
    
    results = search_ticker(request.query)
    return {"results": results}



@app.get("/admin/tickers")
def list_tickers():
    db = SessionLocal()
    tickers = db.query(Ticker).all()
    db.close()
    records=[]
    for ticker in tickers:
        record={
            "symbol":ticker.symbol,
            "name":ticker.name,
        }
        records.append(record)

    return records




#from utils.file_writer import save_comparison_report, save_dataframe_data, save_raw_data_payload