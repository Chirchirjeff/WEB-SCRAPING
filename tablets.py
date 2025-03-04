import requests
from bs4 import BeautifulSoup
import pandas as pd

base_url = "https://webscraper.io/test-sites/e-commerce/static/computers/tablets?page={}"

tablets_data= []

page= 1

while True:
    url= base_url.format(page)
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "lxml")
    tablets= soup.find_all("div", class_= "card thumbnail")

    if not tablets:
        print("No more pages to scrape")
        break

    for tablet in tablets:
        name = tablet.find("a", class_= "title").text.strip()
        price= tablet.find("h4", class_= "price float-end card-title pull-right").text.strip()
        description= tablet.find("p", class_= "description card-text").text.strip()

        tablets_data.append({
            "Name": name,
            "Price": price,
            "Description": description
        })
    page += 1

df= pd.DataFrame(tablets_data)
# print(df)
df.to_excel("tablets_data.xlsx", index= False)




