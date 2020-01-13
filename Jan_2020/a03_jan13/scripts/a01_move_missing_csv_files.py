# Author  : Bhishan Poudel
# Date    :  Jan 7, 2020
import numpy as np
import os
import glob

missing_num = []
START = 700
idir = 'dmstack_csv{}_missing_some'.format(START)
odir = idir.replace('some','only')

if not os.path.isdir(odir):
    os.makedirs(odir)

for i in range(START, START+100):
    l =  idir + '/src_lsst_z1.5_{}.csv'.format(i)
    l9 = l.replace('lsst','lsst90')
    m = l.replace('lsst','lsst_mono')
    m9 = l.replace('lsst','lsst_mono90')

    for f in [l,l9,m,m9]:
        if  not os.path.isfile(f):
            num = f[-7:-4]
            missing_num.append(num)

# collect missing nums
missing_num = sorted(set(missing_num))

print(missing_num)
print(len(missing_num))
print()

# now move missing files
for i in missing_num:
    l =  '{}/src_lsst_z1.5_{}.csv'.format(idir, i)
    l9 = l.replace('lsst','lsst90')
    m = l.replace('lsst','lsst_mono')
    m9 = l.replace('lsst','lsst_mono90')

    for f in [l,l9,m,m9]:
        f2 = f.replace(idir,odir)
        try:
            print(f)
            print(f2)
            print()
            os.rename(f,f2)
        except:
            pass