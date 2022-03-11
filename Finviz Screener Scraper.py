import requests
from bs4 import BeautifulSoup


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

if 'BTO' in screen_good_companies():
    print("it's here!")


