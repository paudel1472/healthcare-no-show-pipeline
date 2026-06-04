from datetime import timedelta
import requests
from bs4 import BeautifulSoup
import pandas as pd 
import os


print("--- [INITIALIZING CORPORATE WEB SCRAPER] ---")

if not os.path.exists('raw_data'):
    os.makedirs('raw_data')

url = "https://books.toscrape.com/catalogue/category/books/sequential-art_5/index.html"

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

print(f"Sending HTTP Request to: {url}...")
response = requests.get(url, headers = headers)

if response.status_code == 200:
    print("✔ Connection Successful! Parsing HTML content...")
    soup = BeautifulSoup(response.text,'html.parser')

    books = soup.find_all('article', class_ = 'product_pod')
    scrapped_data = []

    for book in books:
        title = book.h3.a['title']
        price_text = book.find('p', class_ ='price_color').text
        price = float(price_text.replace('£', '').replace('Â', ''))

        availability_text = book.find('p', class_= 'instock availability').text.strip()
        in_stock = 1 if "In stock" in availability_text else 0

        scrapped_data.append({
            'Product_title': title,
            'Price': price,
            'Availability': in_stock
        
        })

    df = pd.DataFrame(scrapped_data)

    output_file = 'raw_data/scraped_products.csv'
    df.to_csv(output_file, index=False)
    print(f"\n✔ SCRAPING COMPLETE! Extracted {len(df)} live products.")
    print(f"Asset successfully saved to: {output_file}")
    print(df.head())
else:
    print(f"❌ Failed to reach target website. Status Code: {response.status_code}")