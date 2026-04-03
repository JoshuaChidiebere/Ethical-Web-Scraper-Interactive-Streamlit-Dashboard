import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import os
from datetime import datetime

# CONFIG
URL = "https://quotes.toscrape.com/"  # Public demo site for practice (change to real target later)
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"
}
DATA_FOLDER = "data"
os.makedirs(DATA_FOLDER, exist_ok=True)


def scrape_quotes():
    print(f"Starting scrape from {URL}...")

    response = requests.get(URL, headers=HEADERS)
    response.raise_for_status()  # Will raise error if site blocks

    soup = BeautifulSoup(response.text, 'html.parser')

    quotes = []
    quote_elements = soup.find_all('div', class_='quote')

    for element in quote_elements:
        text = element.find('span', class_='text').get_text(strip=True)
        author = element.find('small', class_='author').get_text(strip=True)
        tags = [tag.get_text() for tag in element.find_all('a', class_='tag')]

        quotes.append({
            'Quote': text,
            'Author': author,
            'Tags': ', '.join(tags),
            'Scraped_Date': datetime.now().strftime('%Y-%m-%d %H:%M')
        })
        time.sleep(0.5)  # Polite delay - respect the server

    # Save to CSV
    df = pd.DataFrame(quotes)
    filename = f"quotes_{datetime.now().strftime('%Y%m%d_%H%M')}.csv"
    filepath = os.path.join(DATA_FOLDER, filename)
    df.to_csv(filepath, index=False)

    print(f"✅ Scraped {len(quotes)} quotes and saved to {filepath}")
    return df


if __name__ == "__main__":
    scrape_quotes()