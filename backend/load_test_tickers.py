from database import engine, init_db, Ticker, SessionLocal

def load_test_tickers( replace_existing: bool=False):
    init_db()
    
    tickers = [
        {"symbol": "AAPL", "name": "Apple Inc."},
        {"symbol": "MSFT", "name": "Microsoft Corporation"},
        {"symbol": "GOOGL", "name": "Alphabet Inc."},
        {"symbol": "AMZN", "name": "Amazon.com Inc."},
        {"symbol": "NVDA", "name": "NVIDIA Corporation"},
        {"symbol": "META", "name": "Meta Platforms Inc."},
    ]

    inserted_count = 0
    with SessionLocal.begin() as db:
        if replace_existing:
            print("Deleting existing rows...")
            db.query(Ticker).delete()

        print("Inserting new rows")
        for ticker in tickers:
            if not db.query(Ticker).filter_by(symbol=ticker["symbol"]).first():
                db.add(Ticker(symbol=ticker["symbol"], name=ticker["name"]))
                inserted_count+=1
    
    print(f"Loaded {len(tickers)} tickers into database!")

if __name__ == "__main__":
    load_test_tickers(replace_existing=False)
