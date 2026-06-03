import os
import pandas as pd
from datetime import datetime
import yfinance as yf  # Install via: pip install yfinance

def download_top_20(ticker_symbol):
    print(f"Fetching data for {ticker_symbol}...")
    
    # 1. Fetching ticker data via Yahoo Finance
    ticker = yf.Ticker(ticker_symbol)
    
    try:
        # Get holdings dataframe
        holdings_df = ticker.funds_data.holdings
        
        if holdings_df is None or holdings_df.empty:
            raise ValueError("No holdings data found via API. Switching to fallback.")
            
    except Exception as e:
        print(f"API Fallback: Scraping or using alternative aggregator for {ticker_symbol}")
        # Alternative fallback using stockanalysis or html parsing if API fails
        url = f"https://stockanalysis.com/etf/{ticker_symbol.lower()}/holdings/"
        try:
            tables = pd.read_html(url)
            holdings_df = tables[0] # Usually the first table on the page
        except Exception as html_err:
            print(f"Failed to fetch data: {html_err}")
            return

    # 2. Clean and Filter to Top 20
    # Expected columns usually contain Ticker/Symbol and Format Weight (%)
    holdings_df = holdings_df.head(20)

    # 3. Add timestamping for historical tracking
    runtime_str = datetime.now().strftime("%Y-%m-%d")
    holdings_df['Snapshot_Date'] = runtime_str
    
    # 4. Save to a designated outputs folder
    os.makedirs("holdings_history", exist_ok=True)
    file_path = f"holdings_history/{ticker_symbol}_top20_{runtime_str}.csv"
    holdings_df.to_csv(file_path, index=False)
    
    # Also overwrite a 'latest' file for easy linking/dashboard integrations
    holdings_df.to_csv(f"{ticker_symbol}_top20_latest.csv", index=False)
    print(f"Successfully saved holdings to {file_path}")

if __name__ == "__main__":
    # Replace 'TOPT' or 'SPMO' with your exact ticker if APMO maps to a specific fund
    TARGET_TICKER = "TOPT" 
    download_top_20(TARGET_TICKER)
