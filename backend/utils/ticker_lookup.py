from sqlalchemy.orm import Session
from database import Ticker, SessionLocal

def search_ticker(company_name: str, limit: int = 5):
    db = SessionLocal()
    
    #steps to search
    #1)lowercase company name and format for SQL matching(in this case anything that contains the user input string but remove either % to change search conditions)
    #2)build SQL query
    #3)convert results to list
    try:
        search_term=f"%{company_name.lower()}%"

        #query=db.query(Ticker)
        #query=query.filter(Ticker.name.ilike(search_term)) #case insentitive LIKE
        #query=query.limit(limit)
        #results=query.all()

        results = (
            db.query(Ticker)
            .filter(Ticker.name.ilike(search_term))
            .limit(limit)
            .all()
        )

        database_output=[]
        for ticker in results:
            ticker_dict={
                "symbol":ticker.symbol,
                "name":ticker.name,
            }
            database_output.append(ticker_dict)
        return database_output
    finally:
        db.close()
    