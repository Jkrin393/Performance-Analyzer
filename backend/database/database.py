from sqlalchemy import create_engine, Column, String
from sqlalchemy.orm import sessionmaker, declarative_base
import os

from dotenv import load_dotenv
load_dotenv()

#check environment and set to local DB if in DEV
DATABASE_URL=os.getenv("DATABASE_URL")

if DATABASE_URL is None:
    raise ValueError("DATABASE_URL has not been set")

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False}) 
SessionLocal = sessionmaker( #session factory
    autocommit=False,  
    autoflush=False,    
    bind=engine      
)   
Base = declarative_base() #in Django: class Model(models.Model)

class Ticker(Base):
    __tablename__ = "tickers" 
    symbol = Column(String, primary_key=True, index=True) 
    name = Column(String, index=True)                     

def init_db():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()






#BASE_DIR=Path(__file__).resolve().parent
#DATABASE_PATH=BASE_DIR/"tickers.db"
#DATABASE_URL = f"sqlite:///{DATABASE_PATH}"




#--------------SELF NOTES-------------------------#
#https://docs.sqlalchemy.org/en/20/tutorial/dbapi_transactions.html //creating DB
#https://docs.sqlalchemy.org/en/20/dialects/sqlite.html //

#fastAPI runs multithreaded & async, check same thread locks/unlocks DB to one user
    #autocommit=False,   #must make a call to commit to update
    #autoflush=False,    #same for automatically updating changes
    #bind=engine         #standard conncection to engine

#SessionLocal() creates a new DB session
#endpoint runs
#After response, db.close() runs automatically

##Pathlib
#__file__ = built in var for directory path of current file\
#.resolve() converts to absolute path and .parent gives directory of file


'''
CRUD operations

C
ticker = Ticker(symbol="AAPL", name="Apple")
db.add(ticker)
db.commit()
db.refresh(ticker)

R
db.query(Ticker).filter(Ticker.symbol == "AAPL").first()

D
db.delete(ticker)
db.commit()

----------Django to FastAPI mental model--------------
SQLAlchemy Session = Django ORM + transaction layer
Depends(get_db) = Django’s implicit request DB lifecycle
create_all() = primitive migration
Alembic = Django migrations

'''