from bs4 import BeautifulSoup
from requests import get
import numpy as np
import pandas as pd


url, white_list = "https://www.olx.pl/elektronika/komputery/monitory/slaskie/?page=", ["144", "160", '165', '120', '200', '1ms', '4ms']
black_list = []
output = [[], [], []]

def scrap():
    for i in range(1, 25):
        for monitor in BeautifulSoup(get((url + str(i))).text, 'html.parser').find_all('div', class_='offer-wrapper'):
            if any(word in monitor.strong.text.lower() for word in black_list):
                continue
            elif any(word in monitor.strong.text.lower() for word in white_list):
                output[0].append(monitor.strong.text)
                output[1].append(int(monitor.find('p', class_='price').text.strip().replace(' ','').replace('zł','')))
                output[2].append((monitor.find('a', href=True)['href'].split('#')[0]))

        (lambda df: df())((lambda df=pd.DataFrame(np.transpose(output), columns=['name', 'price', 'url']).drop_duplicates(): df.assign(price=df.price.astype(int)).sort_values(["price"], axis=0, ascending=True).to_csv('janieprzesortuje.csv', sep=';')))


if __name__ == '__main__':
    scrap()
