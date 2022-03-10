from bs4 import BeautifulSoup
import requests
import time

url = 'https://finviz.com/insidertrading.ashx'

# noinspection SpellCheckingInspection
# Headers to bypass forbidden Scraping
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'
}
# Fetch Webpage
raw_html = requests.get(url, headers=headers).text
soup = BeautifulSoup(raw_html, 'lxml')
insider_buying = 'insider-buy-row-2 cursor-pointer'
insider_selling = 'insider-sale-row-2 cursor-pointer'
insider_options_exercises = 'insider-option-row cursor-pointer'

count_com = 0

# Large Insider Buys


def finviz_scrape(flag, directory):
    """
    Scrapes information From the Finviz Insider Trading interface and SEC filings
    :param flag:
    :param directory:
    :return:
    """
    for ticker, trade in enumerate(soup.find_all('tr', class_=flag)):
        global count_com
        count_com += 1
        ticker = trade.find('a', class_='tab-link')
        # print(ticker, '\n')
        name = trade.find('td', style='white-space:nowrap')
        relationship = name.find_next('td', style='white-space:nowrap')
        date_traded = relationship.find_next('td', style='white-space:nowrap')
        cost = trade.find('td', align='right')
        shares = cost.find_next_sibling('td', align='right')
        value = float(cost.text) * int(shares.text.replace(',', ''))
        sec_filing = trade.find('td', style='white-space:nowrap', align='center', onclick='ignoreOnClick=true;').a[
            'href']

        # Fetch Personal Details directly from the SEC Filing

        sec_file = requests.get(sec_filing, headers=headers).text
        sec_soup = BeautifulSoup(sec_file, 'lxml')
        form = sec_soup.find('td', rowspan='3', width='35%', valign='top')
        address = form.find('span', class_='FormData')
        address2 = address.find_next('span', class_='FormData')
        city = address2.find_next('span', class_='FormData')
        state = city.find_next('span', class_='FormData')
        zip_code = state.find_next('span', class_='FormData')

        # Fetch Company Information
        sec_url = f'https://finviz.com/quote.ashx?t={ticker.text}&b=2'
        raw_company_data = requests.get(sec_url, headers=headers).text
        company_soup = BeautifulSoup(raw_company_data, 'lxml')
        company_bio = company_soup.find('td', class_='fullview-profile', align='left')

        # print the output
        with open(f'Insider Trading/{directory}/{ticker.text}', 'w') as f:
            f.write(f'******************* \n')
            f.write('\n')
            f.write(f'Ticker: {ticker.text} \n')
            f.write('\n')
            f.write('\n')
            f.write(f'{company_bio.text}')
            f.write('\n')
            f.write('\n')
            f.write(f'Name: {name.text} \n')
            f.write(f'Filed Address: {address.text} {city.text} {state.text}, {zip_code.text} \n')
            f.write(f'Relationship: {relationship.text} \n')
            f.write(f'Date Traded: {date_traded.text} \n')
            f.write(f'Cost per Share: ${cost.text} \n')
            f.write(f'Shares: {shares.text} \n')
            f.write(f'Value: ${"{:,.2f}".format(value)} \n')
            f.write(f'SEC Filing Form: {sec_filing} \n')
            print(f'Added {ticker.text} to {directory}')


start_time = time.time()
finviz_scrape(insider_buying, 'Large Insider Buys')
finviz_scrape(insider_selling, 'Large Insider Sells')
finviz_scrape(insider_options_exercises, 'Options Exercises')
end_time = time.time()

# Print Confirmation Message
execution_time = '{:.2f}'.format(end_time - start_time)
print(f'{count_com} Insider Trades Scraped in {execution_time} Seconds')
