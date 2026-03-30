#https://fastapi.tiangolo.com/#interactive-api-docs
#https://fastapi.tiangolo.com/python-types/#union

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import router
import os

from dotenv import load_dotenv
load_dotenv()

APLHA_VANTAGE_API_KEY = os.getenv("APLHA_VANTAGE_API_KEY")
ENVIRONMENT=os.getenv("ENVIRONMENT", "development")
LOCAL_FRONTEND_URL = os.getenv("LOCAL_FRONTEND_URL")
VERCEL_FRONTEND_URL=os.getenv("VERCEL_FRONTEND_URL")

app = FastAPI(
    title="Security Analyzer API",
    description="Compare securities and analyze performance metrics",
    version="1.0.0"
)
origins=[]

if ENVIRONMENT=="development":
    origins.append(LOCAL_FRONTEND_URL)

if ENVIRONMENT=="production":
    origins.append(VERCEL_FRONTEND_URL)


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,        #frontend domains
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],          #all headers
    allow_credentials=True,
)


app.include_router(router)