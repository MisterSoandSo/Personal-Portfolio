class Asset:
    """
    Abstract base class representing a generic financial asset.

    This class defines the interface and common attributes for all asset types,
    such as stocks, cryptocurrencies, or bonds. Subclasses should implement their own
    data loading and analysis methods specific to the asset type.
    """
    def __init__(self, symbol, start, end):
        self.symbol = symbol
        self.start_date = start
        self.end_date = end
        self.data = self.load_data()
        self.holdings = 0

    def load_data(self):
        raise NotImplementedError("This should be implemented by subclasses")

    def analyze_data(self):
        raise NotImplementedError("This should be implemented by subclasses")