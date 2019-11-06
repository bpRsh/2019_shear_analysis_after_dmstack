# Author: Bhishan Poudel
# Date:  Nov 1, 2019

import os
import numpy as np
import pandas as pd
import seaborn as sns
sns.set(color_codes=True)

pd.set_option('display.max_columns',200)

import matplotlib.pyplot as plt

if not os.path.isdir('results'):
    os.makedirs('results')


#===============================================================================
colnames = """fN[0][0]       fN[1][0]       fN[2][0]       fN[3][0]
id[0][0]       id[1][0]       id[2][0]       id[3][0]
x[0] x[1]     
errx[0][0]     errx[0][1]     errx[1][0]     errx[1][1]
errx[2][0]     errx[2][1]     errx[3][0]     errx[3][1]
g[0][0]        g[0][1]        g[1][0]        g[1][1] 
g[2][0]        g[2][1]        g[3][0]        g[3][1]
shear[0][0]    shear[1][0]    shear[2][0]    shear[3][0]
flux[0][0]     flux[1][0]     flux[2][0]     flux[3][0]
radius[0][0]   radius[1][0]   radius[2][0]   radius[3][0]
gm[0]          gm[1]          gc[0]          gc[1]
""".split()

colnames = [i.strip() for i in colnames]

#===============================================================================
# final_text is obtained from imcat after combining m,m9,l,l9 text files
df = pd.read_csv('final/final_text.txt',sep=r'\s+',
                 comment='#',header=None)

df.columns = colnames

#===============================================================================
# Find total flux, gm**2 and gc**2
df['flux'] = df['flux[0][0]'] + df['flux[1][0]'] + df['flux[2][0]'] + df['flux[3][0]']
df['gm_sq'] = df['gm[0]']**2 + df['gm[1]']**2
df['gc_sq'] = df['gc[0]']**2 + df['gc[1]']**2

#===============================================================================
df_06_10 = df.query("0.6 < gm_sq < 1.0")

with open('results/a00_output.txt','w') as fo:
    print('all objects = {:,}'.format(len(df)), file=fo)
    print('bad objects = {:,}'.format(len(df_06_10)), file=fo)
    print('bad objects percentage = {:.2f}% '.format(len(df_06_10)/len(df)*100),file=fo )

#===============================================================================
fig, ax = plt.subplots(2,1,figsize=(12,12))

# kde and histogram
df['gm_sq'].plot.kde(ax=ax[0])
df['gm_sq'].hist(ax=ax[1], label='gm_sq',bins=60)

# labels
ax[0].set_xlabel('gm_sq kde')
ax[1].set_xlabel('gm_sq histogram')

# limits
ax[0].set_xlim(0,1.5)
ax[1].set_xlim(0,1.5)

# ticks
ax[0].set_xticks(np.arange(0,1.5,0.1))
ax[1].set_xticks(np.arange(0,1.5,0.1))

# hr lines
ax[0].axhline(y=0,c='g',ls='--', label='density = 0',alpha=0.5)
ax[0].axhline(y=0.25,c='g',ls='--', label='density = 0.25')

# vr lines
ax[0].axvline(x=0.6,c='r',ls='--',label='gmsq = 0.6')
ax[0].axvline(x=1.0,c='r',ls='--', label='gmsq = 1.0')
ax[1].axvline(x=0.6,c='r',ls='--',label='gmsq = 0.6')
ax[1].axvline(x=1.0,c='r',ls='--', label='gmsq = 1.0')

# legends
ax[0].legend()
ax[1].legend()
plt.suptitle('density plot and histogram of gm_sq for all data')
plt.savefig('results/a01_gmsq_kde_whole_data.png')

# zoom y-axis
ax[0].set_ylim(0,0.7)
plt.savefig('results/a02_gmsq_kde_zoom.png')

plt.show()
