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
large_insider_buys = 'insider-buy-row-2 cursor-pointer'
small_insider_buys = 'insider-buy-row-1 cursor-pointer'
large_insider_sells = 'insider-sale-row-2 cursor-pointer'
small_insider_sells = 'insider-sale-row-2 cursor-pointer'
insider_options_exercises = 'insider-option-row cursor-pointer'

lib = []
sib = []
lis = []
sis = []
ioe = []

count_com = 0

# Large Insider Buys


def finviz_scrape(flag, directory, output_list_name):

    """
    Scrapes information From the Finviz Insider Trading interface and SEC filings
    :param flag:
    :param directory:
    :return:
    """
    for ticker, trade in enumerate(soup.find_all('tr', class_=flag)):
        global count_com
        count_com += 1

        # Fetch Basic Trade Info

        ticker = trade.find('a', class_='tab-link')
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

        # Export the output onto text files

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

            output_list_name.append(ticker.text)

def screen_good_companies():
    """
    Returns a list of companies with the following attributes:
     - Return on Equity over 15%
     - Current Ratio over 2
     - Long-Term Debt/Equity Ration under 0.5
     - Dividend Yield over 4%
    :return:
    """

    url = 'https://finviz.com/screener.ashx?v=171&f=fa_curratio_o2,fa_div_o4,fa_ltdebteq_u0.5,fa_roe_o15&ft=4'

    headers = {
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36"
    }

    raw_html = requests.get(url, headers= headers).text
    soup = BeautifulSoup(raw_html, 'lxml')
    good_companies = []

    # Fetch company info

    company_table = soup.find('table', class_ = 'table-light')
    companies = company_table.find_all('tr', valign = 'top')

    for company in companies:

        # Build a List

        ticker = company.find('td', height = '10', align = 'left')
        good_companies.append(ticker.text)
    return good_companies


if __name__ == '__main__':
    while True:
        start_time = time.time()
        print('Fetching Large Insider Buys Info...')
        finviz_scrape(large_insider_buys, 'Large Insider Buys', lib)
        print('Fetching Small Insider Buys Info...')
        finviz_scrape(small_insider_buys, 'Small Insider Buys', sib)
        print('Fetching Large Insider Sells Info...')
        finviz_scrape(large_insider_sells, 'Large Insider Sells', lis)
        print('Fetching Small Insider Buys Info...')
        finviz_scrape(small_insider_sells, 'Small Insider Sells', sis)
        print('Fetching Insider Options Exercise Info...')
        finviz_scrape(insider_options_exercises, 'Options Exercises', ioe)
        end_time = time.time()

        # Print Confirmation Message
        execution_time = '{:.2f}'.format(end_time - start_time)
        print('\n')
        print(f'{count_com} Insider Trades Scraped in {execution_time} Seconds')

        print('Screening For Good Companies:')
        print(screen_good_companies())

        matched = False

        # compare the insider trades with the good companies
        for ticker in screen_good_companies():
            if ticker in lib:
                print(f'{ticker} appears to be a good company being insider bought')
                matched = True
        print('\n')
        if matched == False:
            print('No Matches Yet')

        print('\n')
        minutes_rest = 15
        time.sleep(minutes_rest*60)
