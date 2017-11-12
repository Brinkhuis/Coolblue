"""
Visualize the collected data from www.coolblue.nl
"""

# import section
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# reading data
PRODUCTINFO = pd.read_csv('data/productinfo.csv')

# price distribution per brand
X_PIXELS, Y_PIXELS, DPI = 1500, 1000, 150
X_INCH, Y_INCH = X_PIXELS / DPI, Y_PIXELS / DPI
plt.figure(figsize=(X_INCH, Y_INCH), dpi=DPI)
sns.boxplot(x='price',
            y='brand',
            data=PRODUCTINFO.groupby('brand').filter(lambda x: len(x) > 5),
            palette='PRGn',
            width=0.75).set_title('Price Distribution per Brand')
sns.despine(offset=10, trim=True)
plt.savefig('plots/price_distribution.png')
