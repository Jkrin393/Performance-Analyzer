import pandas as pd
from database import engine, init_db, Ticker, SessionLocal
from sqlalchemy.orm import Session

def load_csv_to_db(csv_path, replace_existing: bool=False):
        
    init_db()
    ticker_df = pd.read_csv(csv_path)
    print(f"Reading CSV from {csv_path}...")
    
    
    with SessionLocal.begin() as db:
        if replace_existing:
            print("Deleting existing rows...")
            db.query(Ticker).delete()

        print("Inserting new rows")
        db.bulk_insert_mappings(
             Ticker,
             ticker_df.to_dict(orient="records")
        )

    print(f"Loaded {len(ticker_df)} tickers into database!")
    
if __name__ == "__main__":
    csv_path = "../data/tickers.csv"
    load_csv_to_db(csv_path)    
    
    """
    db=SessionLocal()        
    
    try:

        tickers = []
        for _,row in ticker_df.iterrows():
            ticker=Ticker(
                symbol=row["symbol"],
                name=row["name"],
            )
            tickers.append(ticker)

        db.bulk_save_objects(tickers)
        db.commit()
        print(f"Loaded {len(ticker_df)} tickers into database!")

    except Exception:
        db.rollback()
        raise
    finally:
         db.close()
    """

