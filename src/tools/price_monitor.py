# src/tools/price_monitor.py

import requests
from bs4 import BeautifulSoup


def scrape_amazon_price(asin):
    # Mock URL for demonstration purposes
    url = f"https://www.amazon.com/dp/{asin}"
    
    # Send a GET request to the URL
    response = requests.get(url)
    
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")
    
    # Find the price element on the page
    price_element = soup.find("span", {"id": "priceblock_ourprice"})
    
    # Extract the price text
    price_text = price_element.text.strip()
    
    # Convert the price text to a float
    price = float(price_text.replace("$", ""))
    
    return price

# Example usage
asin = "B076MX9VG9"
price = scrape_amazon_price(asin)
print(f"Price: ${price:.2f}")