"""
Scraping price information from www.coolblue.nl
"""

import pandas as pd
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

BASE_URL = 'https://www.coolblue.nl/producttype:mobiele-telefoons'


def npages(url):
    """
    Return number of subpages from base url
    """

    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    
    pagination = list()
    for page_number in soup.find_all('span', {'class': 'pagination__link-text'}):
        pagination.append(page_number.text.strip())
    return int(pagination[-2])


def get_productinfo(url):
    """
    Scrape product information per webpage
    """
    
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    
    product_list = list()
    price_list = list()
    rating_list = list()
    review_list = list()
    
    products = soup.find_all('a', {'class': 'product__title js-product-title'})
    for product in products:
        product_list.append(product.text.strip())
    
    prices = soup.find_all('strong', {'class': 'sales-price__current'})
    for price in prices:
        price_list.append(float(price.text.strip().strip(',-').replace('.', '').replace(',', '.')))
    
    ratings = soup.find_all('meter', {'class': 'review-rating--score-meter'})
    for rating in ratings:
        rating_list.append(str(rating).split('value="')[1].split('">')[0])
    
    reviews = soup.find_all('span', {'class': 'review-rating--reviews'})
    for review in reviews:
        review_list.append(int(review.text.strip().strip(' reviews')))

    productinfo = pd.DataFrame({'product': product_list,
                                'price': price_list,
                                'rating': rating_list,
                                'reviews': review_list})
    return productinfo


def main():
    """
    Save scraped product data to file
    """
    
    df = pd.DataFrame()

    for page in tqdm(range(1, npages(BASE_URL) + 1)):
        data = get_productinfo(f'{BASE_URL}?pagina={page}')
        df = pd.concat([df, data])
    
    df['brand'] = df['product'].apply(lambda x: x.strip().split(' ')[0])
    
    file_name = '../data/productinfo.csv'
    
    df.to_csv(file_name, index=False)
    
    print(f'{df.shape[0]} records saved to {file_name}')
    
if __name__ == "__main__":
    main()