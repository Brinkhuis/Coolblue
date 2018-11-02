"""
Visualize the data from www.coolblue.nl
"""

# import section
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# reading data
PRODUCTINFO = pd.read_csv('../data/productinfo.csv')

# set plot dimensions
X_PIXELS, Y_PIXELS, DPI = 1500, 1000, 150
X_INCH, Y_INCH = X_PIXELS / DPI, Y_PIXELS / DPI

# plot price distribution per brand
plt.figure(figsize=(X_INCH, Y_INCH), dpi=DPI)
sns.boxplot(x='price',
            y='brand',
            data=PRODUCTINFO.groupby('brand').filter(lambda x: len(x) > 5),
            order=list(PRODUCTINFO.groupby('brand').filter(lambda x: len(x) > 5)
                       .groupby('brand').price.median().sort_values(ascending=False).index),
            palette='PRGn',
            width=0.75).set_title('Price Distribution per Brand')
sns.despine(offset=10, trim=True)


# save plot
file_name = '../plots/price_distribution_brand.png'
plt.savefig(file_name)
print(f'Visualisation saved to {file_name}')
plt.close()