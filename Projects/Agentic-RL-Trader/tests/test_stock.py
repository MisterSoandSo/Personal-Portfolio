import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from ARLTrader import Stocks

def test_analyze_data_adds_indicators():
    stock = Stocks("AAPL", "2022-01-01", "2022-12-31")
    df = stock.analyze_data()
    assert "SMA_3" in df.columns
    assert "Returns" in df.columns