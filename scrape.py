import pandas as pd
from bs4 import BeautifulSoup
import json
import re
import requests
import random

def download_html(url, filename):
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (iPad; CPU OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (Android 11; Mobile; rv:90.0) Gecko/90.0 Firefox/90.0",
        "Mozilla/5.0 (Android 11; Tablet; rv:90.0) Gecko/90.0 Firefox/90.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:90.0) Gecko/20100101 Firefox/90.0",
    ]
    user_agent = random.choice(user_agents)
    headers = {
        'User-Agent': user_agent,
    }
    try :
        response = requests.get(url, headers=headers, timeout=100)

        if response.status_code == 200:
            with open(filename, 'w', encoding = 'utf-8') as f:
                f.write(response.text)
            print(f"HTML content downloaded and saved to {filename}")
        else:
            print(f"Failed to download HTML. Status code: {response.status_code}")
            print(f"Response text: {response.text}")
            return
        content_length = response.headers.get('content-length')
        if content_length:
            expected_size = int(content_length)
            actual_size = len(response.text)
            if actual_size < expected_size:
                print(f"Downloaded size ({actual_size} bytes) is less than expected size ({expected_size} bytes). ")
                print("Download may be incomplete.")
    except request.exceptions.RequestException as e:
        print(f"Error downloading HTML: {e}")
    except Exception as e:
        print(f"An unexpected error occured: {e}")
if __name__ == "__main__":
    url = "https://www.macrotrends.net/stocks/stock-screener"
    filename = "macrotrends_stock_screener.html"
    download_html(url, filename)


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
with open('macrotrends_stock_screener.html', 'r', encoding='utf-8') as f:
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