"""
Scraping price information from www.coolblue.nl
"""

import pandas as pd
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
RATING = list()
REVIEWS = list()
HIGHLIGHT1 = list()
HIGHLIGHT2 = list()
HIGHLIGHT3 = list()

for page in range(1, npages(BeautifulSoup(requests.get(URL).text,
                                          'html.parser')) + 1):
    soup = BeautifulSoup(requests.get(URL + '?pagina=' + str(page)).text,
                         'html.parser')
    products = soup.find_all('a', {'class': 'product__title js-product-title'})
    for product in products:
        PRODUCT.append(product.text.strip())
        BRAND.append(product.text.strip().split(' ')[0])
    prices = soup.find_all('strong', {'class': 'product__sales-price'})
    for price in prices:
        PRICE.append(float(price.text.strip().strip(',-')
                           .replace('.', '').replace(',', '.')))
    ratings = soup.find_all('meter', {'class': 'review-rating--score-meter'})
    for rating in ratings:
        RATING.append(str(rating).split('value="')[1].split('">')[0])
    reviews = soup.find_all('span', {'class': 'review-rating--reviews'})
    for review in reviews:
        REVIEWS.append(int(review.text.strip().strip(' reviews')))
    highlights = soup.find_all('li', {'class': 'product__highlight'})
    highlight_counter = 1
    for highlight in highlights:
        if highlight_counter == 1:
            HIGHLIGHT1.append(str(highlight).strip('</li>').split('>')[-1])
        if highlight_counter == 2:
            HIGHLIGHT2.append(str(highlight).strip('</li>').split('>')[-1])
        if highlight_counter == 3:
            HIGHLIGHT3.append(str(highlight).strip('</li>').split('>')[-1])
        highlight_counter += 1
        if highlight_counter > 3:
            highlight_counter = 1

PRODUCTINFO = pd.DataFrame({'brand': BRAND,
                            'product': PRODUCT,
                            'price': PRICE,
                            'rating': RATING,
                            'reviews': REVIEWS,
                            'highlight1': HIGHLIGHT1,
                            'highlight2': HIGHLIGHT2,
                            'highlight3': HIGHLIGHT3})
PRODUCTINFO.to_csv('data/productinfo.csv', index=False)
