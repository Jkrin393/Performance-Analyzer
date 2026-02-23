from sqlalchemy import create_engine, Column, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = "sqlite:///./tickers.db"

Base = declarative_base() #in Django: class Model(models.Model)
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False}) #fastAPI runs multithreaded & async, check same thread locks/unlocks DB to one user
SessionLocal = sessionmaker( #session factory
    autocommit=False,   #must make a call to commit to update
    autoflush=False,    #same for automatically updating changes
    bind=engine         #standard conncection to engine
)

class Ticker(Base):
    __tablename__ = "tickers" #explicit declaration of table name
    symbol = Column(String, primary_key=True, index=True) #    symbol = models.CharField(primary_key=True)
    name = Column(String, index=True)                     #    name = models.CharField(db_index=True)

def init_db():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



#--------------SELF NOTES-------------------------#
#https://docs.sqlalchemy.org/en/20/tutorial/dbapi_transactions.html //creating DB
#https://docs.sqlalchemy.org/en/20/dialects/sqlite.html //

#SessionLocal() creates a new DB session
#endpoint runs
#After response, db.close() runs automatically

#unlike DJango built in ORM, fastAPI needs requires explicit management

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