import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from ARLTrader import Portfolio

@pytest.fixture
def setup_portfolio():
    portfolio = Portfolio()
    portfolio.add_cash(10000)
    portfolio.set_period("2022-01-01", "2022-12-31")
    portfolio.add_asset("AAPL")
    return portfolio

def test_add_cash(setup_portfolio):
    setup_portfolio.add_cash(5000)
    assert setup_portfolio.cash == 15000

def test_buy_stock(setup_portfolio):
    portfolio = setup_portfolio
    portfolio.buy("AAPL", "2022-06-01", 10)
    assert portfolio.assets["AAPL"].holdings == 10
    assert portfolio.cash < 10000

def test_sell_stock(setup_portfolio):
    portfolio = setup_portfolio
    portfolio.buy("AAPL", "2022-06-01", 10)
    portfolio.sell("AAPL", "2022-07-01", 5)
    assert portfolio.assets["AAPL"].holdings == 5
    assert portfolio.cash > 0

def test_insufficient_cash(setup_portfolio):
    with pytest.raises(ValueError):
        setup_portfolio.buy("AAPL", "2022-06-01", 1000000)  # Should raise due to insufficient cash

def test_sell_more_than_owned(setup_portfolio):
    setup_portfolio.buy("AAPL", "2022-06-01", 1)
    with pytest.raises(ValueError):
        setup_portfolio.sell("AAPL", "2022-07-01", 10)