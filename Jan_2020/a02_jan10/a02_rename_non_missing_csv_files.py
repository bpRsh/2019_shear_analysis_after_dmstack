# Author  : Bhishan Poudel
# Date    :  Jan 7, 2020
import numpy as np
import os
import shutil
import glob

lsst = ['lsst','lsst90','lsst_mono','lsst_mono90']

START = 700
idir = 'dmstack_csv{}_missing_some'.format(START)
odir =  'dmstack_csv{}_renamed'.format(START)
OLD_END = 250 # Last file of dmstack_txt + one

if not os.path.isdir(odir):
    os.makedirs(odir)

#================================
## sort the file names

# lsst lsst_mono and lsst_mono90
l = sorted(glob.glob('{}/*_lsst_*.csv'.format(idir)))
l = [i for i in l if 'lsst_mono' not in i]
l9 = sorted(glob.glob('{}/*_lsst90_*.csv'.format(idir)))
m = sorted(glob.glob('{}/*_lsst_mono_*.csv'.format(idir)))
m9 = sorted(glob.glob('{}/*_lsst_mono90*.csv'.format(idir)))

# for f in [l,l9,m,m9]:
#     print(f)
#     print(len(f))

##==========================================
## rename files 600 ==>  100
ofile = 'renamed_files{}.txt'.format(START)
if os.path.isfile(ofile):
    os.remove(ofile)
fh = open(ofile,'a')
for lst in [l,l9,m,m9]:
    for i,f in zip(range(OLD_END, OLD_END+len(l)), lst):
        f2 = f.replace(idir,odir)
        num = f[-7:-4]
        f2 = f2.replace(num+'.csv',  str(i)+ '.csv')
        print(f)
        print(f2)
        print(f,file=fh)
        print(f2+'\n\n',file=fh)
        print()
        shutil.copyfile(f,f2)