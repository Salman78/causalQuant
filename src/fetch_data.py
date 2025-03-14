import yfinance as yf
import pandas as pd
import os

def fetch_data(ticker, start_date, end_date):
    """
    Fetch historical market data for a given ticker symbol.
    :param ticker: Ticker symbol (e.g., 'SPY')
    :param start_date: Start date (e.g., '2020-01-01')
    :param end_date: End date (e.g., '2021-01-01')
    :return: DataFrame with historical market data
    """
    data = yf.download(ticker, start=start_date, end=end_date)
    data.reset_index(inplace=True)
    return data

if __name__ == "__main__":
    ticker = "SPY"
    start_date = "2020-01-01"
    end_date = "2021-01-01"
    data = fetch_data(ticker, start_date, end_date)
    
    # Ensure the directory exists
    output_dir = "../data"
    os.makedirs(output_dir, exist_ok=True)
    
    data.to_csv(f"{output_dir}/SPY.csv", index=False)
    print("✅ Data fetched and saved to ../data/SPY.csv")