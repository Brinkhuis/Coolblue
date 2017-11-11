"""
Scraping price information from www.coolblue.nl
to visualize the price distribution per brand.
"""
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import requests
from bs4 import BeautifulSoup

URL = 'https://www.coolblue.nl/producttype:mobiele-telefoons'

def npages(mysoup):
    """
    This functions returns the number of pages of URL.
    """
    pagination = list()
    for page_number in mysoup.find_all('a', {'class': 'pagination__content'}):
        pagination.append(page_number.text.strip())
    return int(pagination[-2])

BRAND = list()
PRODUCT = list()
PRICE = list()

for page in range(1, npages(BeautifulSoup(requests.get(URL).text,
                                          'html.parser')) + 1):
    soup = BeautifulSoup(requests.get(URL + '?pagina=' + str(page)).text,
                         'html.parser')
    products = soup.find_all('a', {'class': 'product__title js-product-title'})
    for product in products:
        PRODUCT.append(str(product.text).strip())
        BRAND.append(str(product.text).strip().split(' ')[0])
    prices = soup.find_all('strong', {'class': 'product__sales-price'})
    for price in prices:
        PRICE.append(float(str(price.text).strip().strip(',-')
                           .replace('.', '').replace(',', '.')))

SMARTPHONES = pd.DataFrame({'price': PRICE,
                            'product': PRODUCT,
                            'brand': BRAND})
SMARTPHONES.to_csv('coolblue.csv', index=False)

X_PIXELS, Y_PIXELS, DPI = 1500, 1000, 150
X_INCH, Y_INCH = X_PIXELS / DPI, Y_PIXELS / DPI
plt.figure(figsize=(X_INCH, Y_INCH), dpi=DPI)
sns.boxplot(x='price',
            y='brand',
            data=SMARTPHONES.groupby('brand').filter(lambda x: len(x) > 5),
            palette='PRGn',
            width=0.75).set_title('Price Distribution per Brand')
sns.despine(offset=10, trim=True)
plt.savefig('coolblue.png')
