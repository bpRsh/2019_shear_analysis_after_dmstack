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
