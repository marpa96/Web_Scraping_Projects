import requests
from bs4 import BeautifulSoup
import pandas as pd

url = 'https://www.zillow.com/homes/Islip,-NY_rb/'

headers = {
    'authority': 'www.zillow.com',
    'method': 'GET',
    'path': "/islip-ny/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3A%22Islip%2C%20NY%22%2C%22mapBounds%22%3A%7B%22west%22%3A-73.2795932067871%2C%22east%22%3A-73.16320679321288%2C%22south%22%3A40.67377468093455%2C%22north%22%3A40.78304760268578%7D%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A395435%2C%22regionType%22%3A6%7D%5D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22sort%22%3A%7B%22value%22%3A%22days%22%7D%2C%22ah%22%3A%7B%22value%22%3Atrue%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A13%7D",
    'scheme': 'https',
    'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    'accept-encoding': "gzip, deflate, br",
    'accept-language': "en-US,en;q=0.9",
    'cache-control': 'max-age=0',
    'referer': "https://www.zillow.com/islip-ny/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3A%22Islip%2C%20NY%22%2C%22mapBounds%22%3A%7B%22west%22%3A-73.27529579640333%2C%22east%22%3A-73.17487389088575%2C%22south%22%3A40.70438064638212%2C%22north%22%3A40.759014424335746%7D%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A395435%2C%22regionType%22%3A6%7D%5D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22sort%22%3A%7B%22value%22%3A%22days%22%7D%2C%22ah%22%3A%7B%22value%22%3Atrue%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A14%7D",
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36'
}

raw_html = requests.get(url, headers=headers).text
soup = BeautifulSoup(raw_html, 'lxml')

# Find the house listing photo card

photo_card = soup.find('article', class_='list-card list-card-additional-attribution list-card-additional-attribution-space list-card_not-saved')
info_json = soup.find('script', type = 'application/ld+json')

#print(soup.find('script', type = 'application/ld+json').text)

# Fetch the house details

price = photo_card.find('div', class_='list-card-price')
address = photo_card.find('address', class_='list-card-addr')
brokerage_firm = photo_card.find('p', class_='list-card-extra-info')

# fetch Quick Details

quick_details = photo_card.find('ul', class_='list-card-details')

bedrooms = quick_details.find('li')
bathrooms = bedrooms.find_next_sibling()
sq_footage = bathrooms.find_next_sibling()

# Fetch More Detailed Link

link = photo_card.find('div', class_ = 'list-card-info').a['href']
print(link)

# Go to that Link

details_raw_html = requests.get(link, headers= headers).text
details = BeautifulSoup(details_raw_html, 'lxml')

# Fetch Overview Information

overview = details.find('div', class_ = 'ds-overview-section')
description = overview.find('div', class_ = 'sc-cxpSdN hXHvzE').find('div', class_ = 'Text-c11n-8-62-5__sc-aiai24-0 sc-bBHxTw kZKvMY efQXcx').fin

listing_price = details.find('span', class_ = 'Text-c11n-8-62-5__sc-aiai24-0 hdp__sc-b5iact-0 frfoXM fAzOKk')

#Fetch Facts And Features

# Output the Results

print(f"""
{address.text}
Brokered by {brokerage_firm.text.split(':')[1]}
*******************************

{description.text}

Asking Price: {listing_price.text}
Bedrooms: {bedrooms.text}
Bathrooms: {bathrooms.text}
Square Footage: {sq_footage.text}
""")