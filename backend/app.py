#https://fastapi.tiangolo.com/#interactive-api-docs
#https://fastapi.tiangolo.com/python-types/#union

from fastapi import FastAPI
from typing import List
from pydantic import BaseModel
from utils.file_writer import save_comparison_report, save_dataframe_data, save_raw_data_payload
from api.alpha_vantage import fetch_multiple_securities
from analysis.metrics import calculate_security_value_metrics, suggest_best_security
from fastapi.middleware.cors import CORSMiddleware

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