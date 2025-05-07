import os
import pandas as pd
import yfinance as yf

from .assets import Asset
CACH_DIR = "stock_data"

class Stocks(Asset):
    """
    Represents a stock asset with historical price data and technical analysis.

    Inherits from the Asset base class and implements stock-specific data loading
    from Yahoo Finance, caching, and technical indicator calculations.

    Attributes:
        symbol (str): The stock ticker symbol.
        start (str): The start date of the data range.
        end (str): The end date of the data range.
        data (pd.DataFrame): Historical stock price data.
        holdings (float): Quantity of this stock held (used in portfolios).
    """
    def load_data(self):
        """
        Loads historical stock data for a given symbol and date range.

        If a local cached CSV file exists, it is loaded. Otherwise, the function
        downloads the data from Yahoo Finance and caches it locally for future use.

        Parameters:
            symbol (str): Stock ticker symbol (e.g., "AAPL", "MSFT").
            start_date (str): Start date for the data in "YYYY-MM-DD" format.
            end_date (str): End date for the data in "YYYY-MM-DD" format.

        Returns:
            pd.DataFrame: A DataFrame containing the historical stock data with columns
                        such as Open, High, Low, Close, Volume, etc.

        Raises:
            RuntimeError: If data cannot be loaded from cache or downloaded from Yahoo Finance.
        """
        if not os.path.exists(CACH_DIR): 
            os.makedirs(CACH_DIR) 

        file_path = f"{CACH_DIR}/{self.symbol}_{self.start_date}_{self.end_date}.csv"
        if os.path.exists(file_path):
            print(f"Loading cached data from: {file_path}")
            try:
                df = pd.read_csv(file_path, skiprows=2, parse_dates=True, index_col=0)
                # Set proper column names
                df.columns = ["Close", "High", "Low", "Open", "Volume"]
                return df
            except Exception as e:
                print(f"Error loading cached data: {e}")
                # fallback to download if cache is corrupted
                pass

        print(f"Downloading data for {self.symbol} from Yahoo Finance...")
        try:
            data = yf.download(self.symbol, start=self.start_date, end=self.end_date)
            if data.empty:
                raise ValueError(f"No data returned for {self.symbol} from {self.start_date} to {self.end_date}")

            df = pd.DataFrame(data)
            df.to_csv(file_path)
            df.columns = ["Close", "High", "Low", "Open", "Volume"]
            return df

        except Exception as e:
            print(f"Failed to download data for {self.symbol}: {e}")
            raise RuntimeError(f"Unable to load or download stock data for {self.symbol}")
        
    def analyze_data(self):
        """
        Enhances stock data with technical indicators, with added safeguards
        for small datasets.

        Returns:
            pd.DataFrame: A DataFrame containing the stock data with technical indicators.
        """
        df = self.data.copy()

        if len(df) < 10:
            print("Warning: Not enough data for full feature engineering. Returning raw data.")
            return df.reset_index(drop=True)

        # Feature engineering
        # Simple Moving Average (SMA) - It is simply the average price over the specified period.
        df['SMA_3'] = df['Close'].rolling(window=3).mean()
        df['SMA_5'] = df['Close'].rolling(window=5).mean()
        df['SMA_10'] = df['Close'].rolling(window=10).mean()
        
        # Calculates the daily percentage change in the stock's closing price.
        df['Returns'] = df['Close'].pct_change()

        # 5-day momentum — the difference between today’s price and the price 5 days ago
        df['Momentum_5'] = df['Close'] - df['Close'].shift(5)

        # This calculates the standard deviation of the past 5 days of returns — a common way to estimate short-term volatility.
        df['Volatility_5'] = df['Returns'].rolling(window=5).std()

        #These are just the closing prices from 1 and 2 days ago.
        df['Lag_1'] = df['Close'].shift(1)
        df['Lag_2'] = df['Close'].shift(2)

        # Drop rows with NaNs caused by rolling/shifting
        df.dropna(inplace=True)
        df.reset_index(drop=True, inplace=True)

        return df
    