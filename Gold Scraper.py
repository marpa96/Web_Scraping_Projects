import time
from datetime import date
from datetime import datetime
from bs4 import BeautifulSoup
import requests
import lxml

headers = {
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'
}

url = 'https://www.kitco.com/charts/livegold.html'

previous_price = 0


def Get_price(previous_price):
    """
    Fetches the current Gold Spot Price from Kitco
    :param previous_price:
    :return:
    """
    raw_html = requests.get(url, headers= headers)
    soup = BeautifulSoup(raw_html.text, 'lxml')
    gold_price = soup.find('div', class_ = 'data-blk bid')
    gp2 = gold_price.find('span').text
    return gp2

previous_price = Get_price(previous_price)

while __name__ == '__main__':

    timemark = datetime.now()
    timestamp = timemark.strftime('%m/%d/%y %H :"%M : %S')

    if previous_price != Get_price(previous_price):
        print(f'${Get_price(previous_price)} at {timemark}')
    previous_price = Get_price(previous_price)
    time_wait = 1
    time.sleep(time_wait)

