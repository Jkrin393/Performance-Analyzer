#https://fastapi.tiangolo.com/#interactive-api-docs
#https://fastapi.tiangolo.com/python-types/#union

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import router
import config


app = FastAPI(
    title="Security Analyzer API",
    description="Compare securities and analyze performance metrics",
    version="1.0.0"
)
origins=[config.LOCAL_FRONTEND_URL]

if config.ENVIRONMENT=="development":
    origins.append(config.LOCAL_FRONTEND_URL)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,        #domains
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],          #all headers
    allow_credentials=True,
)


app.include_router(router)