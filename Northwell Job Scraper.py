import requests
from bs4 import BeautifulSoup

location = 'Islip'
keyword = 'assistant'
url_generator = 'https://jobs.northwell.edu/job-search-results/?keyword=assistant&location=Islip%2C%20NY%2011751%2C%20USA&latitude=40.7267132&longitude=-73.21165839999999&radius=15'

# noinspection SpellCheckingInspection
headers = {
    'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36"
}

raw_html = requests.get(url_generator, headers= headers).text
soup = BeautifulSoup(raw_html, 'html')

jobs = soup.find('div', class_ = 'flex_column av_two_third  flex_column_table_cell av-equal-height-column av-align-top av-zero-column-padding   avia-builder-el-9  el_after_av_one_third  el_before_av_codeblock  search-res-table ')
print(soup.prettify())
