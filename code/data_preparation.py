"""
Add features from scraped raw data
"""
# import section
import pandas as pd

# reading data
PRODUCTINFO = pd.read_csv('data/productinfo_raw.csv')

# feature engineering
PRODUCTINFO['brand'] = PRODUCTINFO['product'].apply(lambda x: x.strip().split(' ')[0])
PRODUCTINFO['os'] = PRODUCTINFO['highlight1'].apply(lambda x:
                                                    x.split(' ')[0] +' ' +
                                                    x.split(' ')[1].split('.')[0]
                                                    if x.startswith(('iOS',
                                                                     'Android',
                                                                     'Cyanogen',
                                                                     'Windows'))
                                                    else '')
PRODUCTINFO['screensize'] = PRODUCTINFO['highlight2'].apply(lambda x:
                                                            float(x.split(' ')[0].replace(',', '.'))
                                                            if x.endswith('scherm')
                                                            else '')
PRODUCTINFO['storage'] = PRODUCTINFO['highlight3'].apply(lambda x:
                                                         x.split(' ')[0] + ' ' + x.split(' ')[1]
                                                         if x.endswith('opslagcapaciteit')
                                                         else '')

# save data preparation
PRODUCTINFO.to_csv('data/productinfo_prep.csv', index=False)
