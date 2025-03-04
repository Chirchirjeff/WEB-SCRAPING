import requests
from bs4 import BeautifulSoup
import pandas as pd

Base_url = "https://www.flipkart.com/search?q=mobiles+under+50000&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&page={}"

phones_data = []
page = 1

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

while True:
    url = Base_url.format(page)
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "lxml")
    phones = soup.find_all("a", class_="CGtC98")

    if not phones:
        break  # Stop loop when no more phones are found

    for phone in phones:
        try:
            phone_name = phone.find("div", class_="KzDlHZ").text.strip()

            # Extract price safely
            price_tag = phone.find("div", class_="Nx9bqj _4b5DiR")
            phone_price = price_tag.text.strip() if price_tag else "Price Not Available"

            phone_description = phone.find("div", class_="_6NESgJ").text.strip()
        except AttributeError:
            continue  # Skip iteration if any attribute is missing

        phones_data.append({
            "Name": phone_name,
            "Price": phone_price,
            "Description": phone_description
        })

    page += 1

df = pd.DataFrame(phones_data)
print(df)
df.to_csv("flipkart_mobiles.csv", index=False)  # Save to CSV
