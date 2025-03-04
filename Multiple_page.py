import requests
from bs4 import BeautifulSoup
import random
import pandas as pd

# List of User-Agents (Real Browser Signatures)
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/98.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/600.8.9 (KHTML, like Gecko) Version/8.0 Safari/600.8.9"
]

# Base URL (Replace `{}` with page number)
BASE_URL = "http://books.toscrape.com/catalogue/page-{}.html"

# Data storage
books_data = []

# Start from Page 1
page = 1

while True:
    url = BASE_URL.format(page)  # Insert current page number into URL
    headers = {"User-Agent": random.choice(user_agents)}  # Pick a random User-Agent

    print(f"Scraping Page {page} | Using User-Agent: {headers['User-Agent']}")

    try:
        response = requests.get(url, headers=headers)

        # Stop if page does not exist
        if response.status_code != 200:
            print("No more pages to scrape. Stopping...")
            break

        soup = BeautifulSoup(response.text, "html.parser")
        books = soup.find_all("article", class_="product_pod")

        if not books:
            print("No books found on this page. Stopping...")
            break

        for book in books:
            title = book.h3.a["title"]
            price = book.find("p", class_="price_color").text.strip()
            availability = book.find("p", class_="instock availability").text.strip()

            books_data.append({"Title": title, "Price": price, "Availability": availability})

        page += 1  # Move to next page

    except requests.exceptions.RequestException as e:
        print(f"Error fetching page {page}: {e}")
        break

# Save data to CSV
df = pd.DataFrame(books_data)
df.to_csv("books_data.csv", index=False)

print("Scraping completed. Data saved to books_data.csv.")
