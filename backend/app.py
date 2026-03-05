#https://fastapi.tiangolo.com/#interactive-api-docs
#https://fastapi.tiangolo.com/python-types/#union

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from utils.ticker_lookup import search_ticker
from database import Ticker, SessionLocal
from routes import router


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


app.include_router(router)