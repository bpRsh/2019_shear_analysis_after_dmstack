Links:
- [a00_e1_vs_e2_plots](https://nbviewer.jupyter.org/github/bpRsh/2019_shear_analysis_after_dmstack/blob/master/Nov_2019/a00_e1_vs_e2_plots.ipynb)
- [a01_e1_e2_dmstack_params](https://nbviewer.jupyter.org/github/bpRsh/2019_shear_analysis_after_dmstack/blob/master/Nov_2019/a01_e1_e2_dmstack_params.ipynb)
- [a03_dmstack_bad_gmsq_density](https://nbviewer.jupyter.org/github/bpRsh/2019_shear_analysis_after_dmstack/blob/master/Nov_2019/a03_dmstack_bad_gmsq_density.ipynb)

# Remove nans from dmstack csv files, select few columns and create txt files
The output of dmstack csv files contains lots of nans. This script will choose only few parameters, does some filterings and remove the nans. From a.csv it gives a.txt file.
```bash
python remove_nans_dmstack.py
```

# Combine four text files to get lc catalog.
We now use imcat command mergecats, which will use some default tolerance to determine the
same objects in two or more lc catalogs and will merge the catalogs. From l.txt, l9.txt, m.txt, and m9.txt we get final/final_000.cat. This final_000.cat is a binary file. We combine all these
binary lc catalog files (final_000.cat to final_099.cat) to a single file final.cat and make it text file `final_text.txt`. This text file has following columns:
```bash
# fN[0][0]       fN[1][0]       fN[2][0]       fN[3][0]
# id[0][0]       id[1][0]       id[2][0]       id[3][0]
# x[0]           x[1]
# errx[0][0]     errx[0][1]     errx[1][0]     errx[1][1]
# errx[2][0]     errx[2][1]     errx[3][0]     errx[3][1]
#
# g[0][0]        g[0][1]        g[1][0]        g[1][1]
# g[2][0]        g[2][1]        g[3][0]        g[3][1]
#
# ellip[0][0]    ellip[1][0]    ellip[2][0]    ellip[3][0]
# flux[0][0]     flux[1][0]     flux[2][0]     flux[3][0]
# radius[0][0]   radius[1][0]   radius[2][0]   radius[3][0]
# gm[0]          gm[1]          gc[0]          gc[1]
```

Note that here g means ellipticity. The reduced shear is g/2.

# Scripts
```python
# Author  : Bhishan Poudel
# Date    : July 5, 2019
# Update  : Oct 29, 2019

# Description:
#===============
# Remove nans from dmstack output csv files and do some filterings to give
# txt files.
#
# Input/Oputputs:
#=================
# Reads all *.csv files and creates *.txt from them.
#
#
# Filtering:
#============
# 1. flag calib_psfCandidate==False
# 2. column deblend_nChild==0
# 3. ellipticity e =  sqrt(e1^2 + e2^2) < 1.5
# 4. choose only few columns given below
# 5. remove nans from all these columns
# 6. change delimiter to tab.
#
#
# Usage:
#=======
# python remove_nans_dmstack.py
#
# Estimated time: 1m 2s
#
import pandas as pd
import numpy as np
import sys
import glob

import multiprocessing
from multiprocessing import Process

def remove_nans(ifile,file_number):
    """ Remove nans and filter data from dmstack output csv file.

    There are 90 flags col0 to col89
    col90 is id is first column 'id'

    There are 90 flags and 77 columns.
    We exclude first column 'flags' and have 76 columns
    In total there are 90 + 76 = 166 columns.

    Columns selected:
    1   :  calib_psfCandidate (for filtering only)
    94  :  deblend_nChild (for filtering only)
    90  :  id
    102 :  base_SdssCentroid_x
    103 :  base_SdssCentroid_y
    104 :  base_SdssCentroid_xSigma
    105 :  base_SdssCentroid_ySigma
    127 :  ext_shapeHSM_HsmShapeRegauss_e1
    128 :  ext_shapeHSM_HsmShapeRegauss_e2
    114 :  ext_shapeHSM_HsmShapeRegauss_sigma

    # Added later for radius calculation
    133: 'ext_shapeHSM_HsmSourceMoments_xx',
    134: 'ext_shapeHSM_HsmSourceMoments_yy',
    135: 'ext_shapeHSM_HsmSourceMoments_xy',

    # This gives
    radius = (xx*yy - xy**2)**1/4

    # In the output  file we have
    # 1          2    34   56             78     9     10    11
    file_number, id,  x,y  xsigma,ysigma, e1,e2, ellip flux, radius
    """

    usecols = [1, 94, 90, 102, 103, 104, 105, 127, 128, 114, 133,134,135]

    df = pd.read_csv(ifile, sep=",",low_memory=False,usecols=usecols)


    for c in df.columns:
        df[c] = pd.to_numeric(df[c],errors='coerce')


    # filter the flag calib_psfCandidate==False
    # not a star candidate
    df = df.query('calib_psfCandidate == 0.0')

    # filter the column deblend_nChild==0
    # no child source after deblending
    df = df.query('deblend_nChild == 0.0')
    df = df.copy()

    # clean out unphysical results
    # e1^2 + e2^2 < 1.5^2
    df['ellip'] = (df['ext_shapeHSM_HsmShapeRegauss_e1'] ** 2 + df['ext_shapeHSM_HsmShapeRegauss_e2'] ** 2)**0.5
    df = df.query('ellip < 1.5')

    # calculate radius of ellipse using HSM moments
    # radius**4 = xx*yy - xy**2
    df['radius'] =  df.eval(""" ( (ext_shapeHSM_HsmSourceMoments_xx *  ext_shapeHSM_HsmSourceMoments_yy) \
                                              -  (ext_shapeHSM_HsmSourceMoments_xy**2 ) )**0.25 """)

    # add a new column with file_number
    df['file_number'] = file_number

    # take only required columns
    cols_select = ['file_number', 'id',
           'base_SdssCentroid_x', 'base_SdssCentroid_y',
           'base_SdssCentroid_xSigma','base_SdssCentroid_ySigma',
           'ext_shapeHSM_HsmShapeRegauss_e1','ext_shapeHSM_HsmShapeRegauss_e2',
           'ellip', 'base_SdssShape_flux',  'radius'
           ]

    df = df[cols_select]

    # drop all nans
    df = df.dropna()

    # write txt file with commented header
    prefix = ' '*2
    header_line = prefix.join(cols_select)

    # from: dmstack_csv/src_lsst_mono_z1.5_000.csv
    # to  : dmstack_txt/src_lsst_mono_z1.5_000.txt
    ofile = ifile.replace('dmstack_csv', 'dmstack_txt')
    ofile = ofile.replace('.csv', '.txt')
    np.savetxt(ofile,df.values,header=header_line,delimiter='\t')

def func1():
    infiles = ['dmstack_csv/src_lsst_z1.5_{:03d}.csv'.format(i) for i in range(100)]
    for ifile in infiles:
        file_number = int(ifile.rstrip('.csv').split('_')[-1])
        remove_nans(ifile, file_number)

def func2():
    infiles = ['dmstack_csv/src_lsst90_z1.5_{:03d}.csv'.format(i) for i in range(100)]
    for ifile in infiles:
        file_number = int(ifile.rstrip('.csv').split('_')[-1])
        remove_nans(ifile, file_number)


def func3():
    infiles = ['dmstack_csv/src_lsst_mono_z1.5_{:03d}.csv'.format(i) for i in range(100)]
    for ifile in infiles:
        file_number = int(ifile.rstrip('.csv').split('_')[-1])
        remove_nans(ifile, file_number)


def func4():
    infiles = ['dmstack_csv/src_lsst_mono90_z1.5_{:03d}.csv'.format(i) for i in range(100)]
    for ifile in infiles:
        file_number = int(ifile.rstrip('.csv').split('_')[-1])
        remove_nans(ifile, file_number)


if __name__ == '__main__':
    p1 = Process(target=func1)
    p1.start()

    p2 = Process(target=func2)
    p2.start()

    p3 = Process(target=func3)
    p3.start()

    p4 = Process(target=func4)
    p4.start()

    # join them all
    p1.join()
    p2.join()
    p3.join()
    p4.join()

```

```bash
# Author  : Bhishan Poudel
# Date    : July 5, 2019
# Update  : Oct 29, 2019

# Description:
#==============
# 
# Usage: bash combine_four_txts_to_lc_catalog.sh
#
# Outputs:
#=========
# Inputs : l.txt, l9.txt, m.txt, m9.txt and gives final/final_000.txt
# Main output: final/final_text.txt
# Temp output: catalogs/*.cat
#
# Detail description:
# ====================
#
# Example .txt has following columns:
#
# column 0,1   : fN     = file_number, id = id
# column 2,3   : x      = base_SdssCentroid_x, base_SdssCentroid_y
# column 4,5   : errx   = base_SdssCentroid_xSigma, base_SdssCentroid_ySigma
# column 6,7,8 : ellip  = ext_shapeHSM_HsmShapeRegauss_e1, ext_shapeHSM_HsmShapeRegauss_e2, ellip
# column 9     : flux   = base_SdssShape_flux
# column 10    : radius = 4th root of (xx*xy - xy*xy)
#
# Output File
#=========================
# fN[0][0]       fN[1][0]       fN[2][0]       fN[3][0]
# id[0][0]       id[1][0]       id[2][0]       id[3][0]
# x[0]           x[1]
# errx[0][0]     errx[0][1]     errx[1][0]     errx[1][1]
# errx[2][0]     errx[2][1]     errx[3][0]     errx[3][1]
#
# g[0][0]        g[0][1]        g[1][0]        g[1][1]
# g[2][0]        g[2][1]        g[3][0]        g[3][1]
#
# ellip[0][0]    ellip[1][0]    ellip[2][0]    ellip[3][0]
# flux[0][0]     flux[1][0]     flux[2][0]     flux[3][0]
# radius[0][0]   radius[1][0]   radius[2][0]   radius[3][0]
# gm[0]          gm[1]          gc[0]          gc[1]
#
#
#==================================================
# NOTE: Here the symbol g is actually ellipticiy e.
#       If we need to calculate reduced shear, then for the weak lensing
#       limit g = e/2
#       i.g. reduced shear g = g/2
#==================================================

z=1.5
BEGIN=0
END=99 # end is included

# main output folder
mkdir -p final
mkdir -p catalogs

# loop through range of files
for i in $(seq -f "%03g" $BEGIN $END)
do
    # texts
    LT="dmstack_txt/src_lsst_z${z}_${i}"
    L9T="dmstack_txt/src_lsst90_z${z}_${i}"
    MT="dmstack_txt/src_lsst_mono_z${z}_${i}"
    M9T="dmstack_txt/src_lsst_mono90_z${z}_${i}"
    
    # catalogs
    LC="catalogs/src_lsst_z${z}_${i}"
    L9C="catalogs/src_lsst90_z${z}_${i}"
    MC="catalogs/src_lsst_mono_z${z}_${i}"
    M9C="catalogs/src_lsst_mono90_z${z}_${i}"

    # create lc catalog from text file
    # in imcat we must read all columns
    # unused columns further: id flux radius
    #echo "Creating: .cat files";
    lc -C -n fN -n id -N '1 2 x' -N '1 2 errx' -N '1 2 g' -n ellip -n flux -n radius < "${LT}".txt > "${LC}".cat
    lc -C -n fN -n id -N '1 2 x' -N '1 2 errx' -N '1 2 g' -n ellip -n flux -n radius < "${L9T}".txt > "${L9C}".cat

    lc -C -n fN -n id -N '1 2 x' -N '1 2 errx' -N '1 2 g' -n ellip -n flux -n radius < "${MT}".txt > "${MC}".cat
    lc -C -n fN -n id -N '1 2 x' -N '1 2 errx' -N '1 2 g' -n ellip -n flux -n radius < "${M9T}".txt > "${M9C}".cat

    # merge the 4 catalogs to a single catalog
    # Make sure mergecats have mono files first and then chromatic files later
    # to comply with the command to create final.cat.
    #echo "Creating: merge.cat"
    mergecats 5 "${MC}".cat "${M9C}".cat "${LC}".cat "${L9C}".cat > merge.cat &&
    #echo "Created: merge.cat"

    # convert the merge catalog into a catalog with mono and color shear values with the 0 degree and 90 degree values averaged:
    #echo "Creating: final.cat";
    lc -b +all 'x = %x[0][0] %x[1][0] + %x[2][0] + %x[3][0] + 4 / %x[0][1] %x[1][1] + %x[2][1] + %x[3][1] + 4 / 2 vector' 'gm = %g[0][0] %g[1][0] + 2 / %g[0][1] %g[1][1] + 2 / 2 vector' 'gc = %g[2][0] %g[3][0] + 2 / %g[2][1] %g[3][1] + 2 / 2 vector' < merge.cat > final/final_${i}.cat

    echo "Created: final/final_${i}.cat"
done;

# combine all final catalogs
cd final;
catcats *.cat > final.cat

# convert binary to text
lc -O < final.cat > final_text.txt 

# remove temp file
rm ../merge.cat

```
