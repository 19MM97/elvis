# -*- coding: utf-8 -*-
"""
Created on Tue Jun 18 14:43:14 2019

@author: draz
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

df = pd.DataFrame(index=range(14 * 60), columns=range(6 * 60, 22 * 60, 60))

df.iloc[1 * 60, :] = np.array([65, 40, 89, 113, 109, 125, 146, 145, 189, 150, 138, 115, 65, 63, 58, 172]) / 2
df.iloc[4 * 60, :] = np.array([44, 72, 130, 209, 228, 205, 159, 179, 214, 238, 221, 127, 74, 56, 76, 91]) / 3
df.iloc[8 * 60, :] = np.array([43, 128, 347, 493, 578, 600, 591, 567, 486, 387, 316, 186, 114, 86, 68, 53]) / 4
df.iloc[13 * 60, :] = np.array([82, 170, 272, 322, 342, 346, 351, 359, 359, 330, 286, 245, 154, 100, 81, 58]) / 5
df.iloc[13 * 60, :] = np.zeros(16)

for c in df:
    df.loc[:, c] = pd.to_numeric(df.loc[:, c]).interpolate(method='linear', limit_direction='both')

df = df.reindex(columns=range(6 * 60, 22 * 60))

for ix, row in df.iterrows():
    df.loc[ix, :] = row.interpolate(method='linear', limit_direction='both')
df = df.reindex(index=df.index[::-1])

arr = np.ceil(pd.DataFrame(df.sum(axis=1)))
arr = arr.tolist()
arr.columns = ['count']
arr = arr.reindex(index=arr.index[::-1])
arr['hour'] = arr.index // 60
arr['cat'] = np.NaN
arr.loc[arr.hour.isin([0, 1]), 'cat'] = 0
arr.loc[arr.hour.isin([2, 3, 4]), 'cat'] = 1
arr.loc[arr.hour.isin([5, 6, 7, 8]), 'cat'] = 2
arr.loc[arr.hour.isin([9, 10, 11, 12, 13, 14]), 'cat'] = 3

ax = arr.groupby('cat')['count'].sum().plot()
ax.set_xticks(range(0, 4))
ax.set_xticklabels(['<2 Std.', '2-4 Std.', '5-8 Std.', '>9 Std.'],  rotation=0)

plt.savefig('percategory.png')
