import pandas as pd
from bs4 import BeautifulSoup
import json
import re

class Stock:
    def __init__(self, name, ticker, industry, market_cap, closing_price, one_year_percent_change, pe_ratio, dividend_yield):
        self.name = name
        self.ticker = ticker
        self.industry = industry
        self.market_cap = market_cap
        self.closing_price = closing_price
        self.one_year_percent_change = one_year_percent_change
        self.pe_ratio = pe_ratio
        self.dividend_yield = dividend_yield

    def __repr__(self):
        return (f"Stock(name={self.name}, ticker={self.ticker}, industry={self.industry}, "
                f"market_cap={self.market_cap}, closing_price={self.closing_price}, "
                f"one_year_percent_change={self.one_year_percent_change}, "
                f"pe_ratio={self.pe_ratio}, dividend_yield={self.dividend_yield})")

# Load the HTML file
with open('data.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

# Parse the HTML content with BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

rows = soup.find_all('div', id=re.compile(r'row([1-9]|1[0-8])jqxGrid'))

stocks = []

for row in rows:
    divs_with_margin_top = row.find_all('div', style=lambda value: value and 'margin-top' in value)
    values = []
    for div in divs_with_margin_top:
        values.append(div.get_text(strip=True))
    stock = Stock(values[0], values[1], values[2], values[3], values[4], values[5], values[6], values[7])
    print(stock)
    stocks.append(stock)

print("stocks size = ", len(stocks))