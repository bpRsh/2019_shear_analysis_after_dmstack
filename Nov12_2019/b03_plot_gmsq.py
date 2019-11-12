# Author: Bhishan Poudel
# Date:  Nov 7, 2019
# Command: py b03_plot_gmsq.py [0]

import scipy
import os,sys,json
import numpy as np
import pandas as pd
import seaborn as sns
sns.set(color_codes=True)

pd.set_option('display.max_columns',200)

import matplotlib.pyplot as plt

# global variables
dict_flags_all = json.load(open('dict_flags.json'))

# arguments
lst_flag_nums_str = sys.argv[1] # [0], [0,1] etc
lst_flag_nums = eval(lst_flag_nums_str)

ofile_whole = ['results/flag/flag_' + '_'.join([str(i) for i in lst_flag_nums])][0] 
ofile_whole = ofile_whole + '.png'

ofile_zoom = ['results/zoom/zoom_' + '_'.join([str(i) for i in lst_flag_nums])][0] 
ofile_zoom = ofile_zoom + '.png'

ofile_text = ['results/text/zoom_' + '_'.join([str(i) for i in lst_flag_nums])][0] 
ofile_text = ofile_text + '.txt'

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
ellip[0][0]    ellip[1][0]    ellip[2][0]    ellip[3][0]
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
a,b = 0.5, 1.1
df_bad = df.query(" @a < gm_sq < @b")


obj_all = 'all objects = {:,}'.format(len(df))
obj_bad = 'bad objects = {:,}'.format(len(df_bad))
per_bad = 'bad objects percentage = {:.4f}% '.format(len(df_bad)/len(df)*100)

with open(ofile_text,'w') as fo:
    line = obj_all + ' ' + obj_bad + ' ' + per_bad + '\n'
    fo.write(line)

# whole figure Histogram
#===============================================================================
fig, ax = plt.subplots(1,1,figsize=(12,12))

# hist + density
g = sns.distplot(df['gm_sq'], bins=60, ax=ax, norm_hist=True, kde=True)

# text
ax.text(0.6,0.4,obj_all)
ax.text(0.6,0.6,obj_bad)
ax.text(0.6,0.8,per_bad)

# labels
ax.set_xlabel('gm_sq')
ax.set_ylabel('arbitrary density unit')

# limits
ax.set_xlim(0,1.5)

# ticks
ax.set_xticks(np.arange(0,1.5,0.1))


# vr lines
ax.axvline(x=a,c='r',ls='--',label=f'gmsq = {a}')
ax.axvline(x=b,c='r',ls='--', label=f'gmsq = {b}')

# legends
ax.legend()
plt.suptitle('Histogram for gmsq')
plt.savefig(ofile_whole)
plt.close()

# zoom y-axis
#================================================
fig, ax = plt.subplots(1,1,figsize=(12,12))
df['gm_sq'].hist(ax=ax, label='gm_sq',bins=60)

# text
ax.text(0.6,4000,obj_all)
ax.text(0.6,4200,obj_bad)
ax.text(0.6,4400,per_bad)

# labels
ax.set_xlabel('gm_sq')
ax.set_ylabel('count')

# limits
ax.set_xlim(0,1.5)


# vr lines
ax.axvline(x=a,c='r',ls='--',label=f'gmsq = {a}')
ax.axvline(x=b,c='r',ls='--', label=f'gmsq = {b}')

# legends
ax.legend()
plt.suptitle('Histogram for gmsq')

# ticks
y_top = 10_000
ax.set_xlim(0.1,1.5)
ax.set_ylim(0,y_top)
ax.set_yticks(np.arange(0,y_top,200))
ax.set_xticks(np.arange(0,1.5,0.1))

for x in np.arange(0,y_top,200):
    ax.axhline(y=x,color='g',alpha=0.3)

plt.savefig(ofile_zoom)
plt.close()
