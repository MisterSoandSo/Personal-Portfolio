from .stocks import Stocks

class Portfolio:
    """
    Represents a user's financial portfolio composed of various assets.

    This class provides functionality to manage available cash, track asset holdings 
    (such as stocks or other future asset types), perform simulated buy/sell operations, 
    and calculate the total portfolio value over time.

    Assets are expected to follow a common interface (e.g., having `data`, `holdings`, 
    and a way to access prices by date). The Portfolio currently supports Stocks, but can 
    be extended to handle other asset classes.

    Attributes:
        assets (dict): A dictionary mapping asset symbols to asset instances (e.g., Stocks).
        cash (float): The amount of unallocated cash in the portfolio.
        period (list[str]): The date range [start_date, end_date] used when initializing assets.

    Methods:
        set_period(start, end): Sets the date range for retrieving asset data.
        add_cash(amount): Increases the cash balance of the portfolio.
        add_asset(symbol): Adds a new asset to the portfolio for the given symbol.
        buy(symbol, date, quantity): Executes a simulated purchase of an asset.
        sell(symbol, date, quantity): Executes a simulated sale of an asset.
        total_value(date): Computes the total value of the portfolio on the specified date.
    """
    def __init__(self):
        self.assets = {}  # Dictionary to hold Asset instances keyed by symbol
        self.cash = 0.0
        self.period = None

    def add_cash(self, amount: float):
        """
        Increases the cash balance of the portfolio.
        """
        self.cash += amount

    def add_asset(self, symbol: str, start: str = None, end: str = None):
        """
        Adds a new asset to the portfolio for the given symbol.

        If start and end dates are provided, they are used to load the asset data.
        Otherwise, the portfolio's default period (self.period) must be set.

        Parameters:
            symbol (str): The ticker symbol of the asset.
            start (str, optional): Custom start date for the asset data.
            end (str, optional): Custom end date for the asset data.

        Raises:
            ValueError: If no date range is provided and no default period is set.
        """
        if start and end:
            asset = Stocks(symbol, start, end)
        elif self.period:
            asset = Stocks(symbol, self.period[0], self.period[1])
        else:
            raise ValueError("Please provide a date range or set the portfolio period first.")
        
        self.assets[symbol] = asset
        
    def set_period(self, start: str, end: str):
        """
        Sets the date range for retrieving asset data.
        """
        self.period = [start,end]

    def buy(self, symbol: str, date: str, quantity: float):
        """
        Executes a simulated purchase of an asset.
        """
        if symbol not in self.assets:
            raise ValueError(f"{symbol} is not in the portfolio.")
        
        asset = self.assets[symbol]
        try:
            price = asset.data.loc[date]['Close']
        except KeyError:
            raise ValueError(f"No price data for {symbol} on {date}")

        cost = price * quantity
        if self.cash < cost:
            raise ValueError("Insufficient cash to complete purchase.")

        self.cash -= cost
        asset.holdings += quantity

    def sell(self, symbol: str, date: str, quantity: float):
        """
        Executes a simulated sale of an asset.
        """
        if symbol not in self.assets:
            raise ValueError(f"{symbol} is not in the portfolio.")
        
        asset = self.assets[symbol]
        if asset.holdings < quantity:
            raise ValueError(f"Not enough holdings of {symbol} to sell.")

        try:
            price = asset.data.loc[date]['Close']
        except KeyError:
            raise ValueError(f"No price data for {symbol} on {date}")

        revenue = price * quantity
        self.cash += revenue
        asset.holdings -= quantity

    def total_value(self, date: str) -> float:
        """
        Computes the total value of the portfolio on the specified date.
        """
        total = self.cash
        for symbol, asset in self.assets.items():
            try:
                price = asset.data.loc[date]['Close']
                total += price * asset.holdings
            except KeyError:
                continue  # If price data is missing for a date, skip it
        return total

    def __repr__(self):
        holdings = {sym: s.holdings for sym, s in self.assets.items()}
        return f"Portfolio(cash={self.cash:.2f}, holdings={holdings})"
