import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import requests

from bs4 import BeautifulSoup

url = 'https://www.coolblue.nl/producttype:mobiele-telefoons'


def npages(soup):
    pages = list()
    for page in soup.find_all('a', {'class': 'pagination__content'}):
        pages.append(page.text.strip())
    return int(pages[-2])


brand_list = list()
product_list = list()
price_list = list()

for page in range(1, npages(BeautifulSoup(requests.get(url).text,
                                          'html.parser')) + 1):
    soup = BeautifulSoup(requests.get(url + '?pagina=' + str(page)).text,
                         'html.parser')
    products = soup.find_all('a', {'class': 'product__title js-product-title'})
    for product in products:
        product_list.append(str(product.text).strip())
        brand_list.append(str(product.text).strip().split(' ')[0])
    prices = soup.find_all('strong', {'class': 'product__sales-price'})
    for price in prices:
        price_list.append(float(str(price.text).strip().strip(',-')
                                .replace('.', '').replace(',', '.')))

df = pd.DataFrame({'price': price_list,
                   'product': product_list,
                   'brand': brand_list})

sns.boxplot(x="price",
            y="brand",
            data=df.groupby('brand').filter(lambda x: len(x) > 5),
            palette="PRGn",
            width=0.8).set_title("Price Distribution per Brand")
sns.despine(offset=10, trim=True)
plt.show()
