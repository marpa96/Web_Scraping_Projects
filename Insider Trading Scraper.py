from bs4 import BeautifulSoup
import requests
import lxml

url = 'https://finviz.com/insidertrading.ashx'

# noinspection SpellCheckingInspection
# Headers to bypass forbidden Scraping
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'
}
# Fetch Webpage
raw_html = requests.get(url, headers= headers).text
soup = BeautifulSoup(raw_html, 'lxml')
insider_buying = soup.find_all('tr', class_ = 'insider-buy-row-2 cursor-pointer')

# Fetch Details
for trade in insider_buying:
    ticker = trade.find('a', class_ = 'tab-link')
    print(ticker, '\n')
    name = trade.find('td', style = 'white-space:nowrap')
    relationship = name.find_next('td', style = 'white-space:nowrap')
    date_traded = relationship.find_next('td', style = 'white-space:nowrap')
    cost = trade.find('td', align = 'right')
    shares = cost.find_next_sibling('td', align = 'right')
    value = float(cost.text)*int(shares.text.replace(',', ''))
    sec_filing = trade.find('td', style = 'white-space:nowrap', align = 'center',onclick = 'ignoreOnClick=true;').a['href']

    # print the output
    print(f'''
    LARGE INSIDER BUY
    *******************

    Ticker: {ticker.text}
    Name: {name.text}
    Relationship: {relationship.text}
    Date Traded: {date_traded.text}
    Cost per Share: ${cost.text}
    Shares: {shares.text}
    Value: ${'{:,.2f}'.format(value)}
    SEC Filing Form: {sec_filing}
    ''')
