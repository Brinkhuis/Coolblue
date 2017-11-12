"""
Visualize the collected data from www.coolblue.nl
"""
# import section
import pandas as pd

# reading data
PRODUCTINFO = pd.read_csv('data/productinfo_raw.csv')

# feature engineering
PRODUCTINFO['os'] = PRODUCTINFO['highlight1'].apply(lambda x:
                                                    x.split(' ')[0] + ' ' + x.split(' ')[1]
                                                    if x.startswith(('iOS',
                                                                     'Android',
                                                                     'Cyanogen',
                                                                     'Windows',
                                                                     'Merkgebonden'))
                                                    else '')
PRODUCTINFO['screensize'] = PRODUCTINFO['highlight2'].apply(lambda x:
                                                            x.split(' ')[0] + ' ' + x.split(' ')[1]
                                                            if x.endswith('scherm')
                                                            else '')
PRODUCTINFO['storage'] = PRODUCTINFO['highlight3'].apply(lambda x:
                                                         x.split(' ')[0] + ' ' + x.split(' ')[1]
                                                         if x.endswith('opslagcapaciteit')
                                                         else '')

# save data preparation
PRODUCTINFO.to_csv('data/productinfo_prep.csv', index=False)
