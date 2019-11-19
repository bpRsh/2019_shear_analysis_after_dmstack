# Author  : Bhishan Poudel
# Date    : July 5, 2019
# Update  : Nov 7, 2019

# Description:
#===============
# Remove nans from dmstack output csv files and
# do some filterings to give txt files.
#
# Input/Oputputs:
#=================
# inputs : ../data/dmstack_csv/*.csv  (100*4 csv files)
# outputs: dmstack_txt/*.txt (100 combined txt files with few columns)
#
# Filtering:
#============

# 1. column ==> deblend_nChild==0
# 2. flag ==> calib_psfCandidate==False **Read flag from json**
# 3. ellipticity  ==> e =  sqrt(e1^2 + e2^2) < 1.5
# 4. selection ==> choose only few columns
# 5. nans ==> remove nans from all selected columns
# 6. delimiter ==> change delimiter from space to tab for imcat
#
# Shape HSM Filtering:
#======================
# Nov 19, 2019
# Reference: https://github.com/LSSTDESC/DC2-analysis/blob/master/tutorials/object_gcr_2_lensing_cuts.ipynb
#
# 7. 'ext_shapeHSM_HsmShapeRegauss_resolution >= 0.3'
# 8. 'ext_shapeHSM_HsmShapeRegauss_sigma <= 0.4'
#
# Usage:
#=======
# py b01_remove_nans_dmstack.py
#
#
# Note: 
# When reading columns ext_shapeHSM_HsmShapeRegauss_e1 and e2
# we read them combinedly as g in IMCAT, so original
# reduced shear will be g = g/2.
#
import pandas as pd
import numpy as np
import os,sys
import glob
import json

import multiprocessing
from multiprocessing import Process

# constants
RANGE = 100

# global variables
dict_flags_all = json.load(open('dict_flags.json'))


# create output folder if not exist
if not os.path.isdir('dmstack_txt'):
    os.makedirs('dmstack_txt')

def remove_nans(ifile,file_number):
    """ Remove nans and filter data from dmstack output csv file.

    There are 90 flags col0 to col89
    col90 is id is first column 'id'

    There are 90 flags and 77 columns.
    We exclude first column 'flags' and have 76 columns
    In total there are 90 + 76 = 166 columns.

    Columns selected:
    # flags only for filtering
    1   :  calib_psfCandidate (for filtering only)
    94  :  deblend_nChild (for filtering only)
    
    # actual columns used
    90  :  id
    102 :  base_SdssCentroid_x
    103 :  base_SdssCentroid_y
    104 :  base_SdssCentroid_xSigma
    105 :  base_SdssCentroid_ySigma
    114 : 'base_SdssShape_flux', 
    127 :  ext_shapeHSM_HsmShapeRegauss_e1
    128 :  ext_shapeHSM_HsmShapeRegauss_e2
    
    # Added on Nov19, 2019 for shape measurements
    # https://github.com/LSSTDESC/DC2-analysis/blob/master/tutorials/object_gcr_2_lensing_cuts.ipynb
    129: 'ext_shapeHSM_HsmShapeRegauss_sigma',
    130: 'ext_shapeHSM_HsmShapeRegauss_resolution',
    
    # Added for radius calculation
    133: 'ext_shapeHSM_HsmSourceMoments_xx',
    134: 'ext_shapeHSM_HsmSourceMoments_yy',
    135: 'ext_shapeHSM_HsmSourceMoments_xy',

    # This gives
    radius = (xx*yy - xy**2)**1/4

    # In the output  file we have
    # 1          2    34   56             78     9     10    11
    file_number, id,  x,y  xsigma,ysigma, e1,e2, ellip flux, radius
    """

    df = pd.read_csv(ifile, sep=",",low_memory=False)
    df.columns = df.columns.str.lstrip('# ')
    
    # make dtype float
    df = df.astype(float)  

    # select only few columns
    usecols = [1, 94, 90, 102, 103, 104, 105,
               127, 128, 129, 130, 114, 133, 134, 135]
    df = df.iloc[:,usecols]
    df = df.copy()

    # make selected columns numeric
    for c in df.columns:
        df[c] = pd.to_numeric(df[c],errors='coerce')


    # filter the flag calib_psfCandidate==False
    # not a star candidate
    df = df.query('calib_psfCandidate == 0.0')

    # filter the column deblend_nChild==0
    # no child source after deblending
    df = df.query('deblend_nChild == 0.0')
    
    
    # filter for HSM shapes
    df = df.query('ext_shapeHSM_HsmShapeRegauss_resolution >= 0.3')
    df = df.query('ext_shapeHSM_HsmShapeRegauss_sigma <= 0.4')

    # clean out unphysical results
    # e1^2 + e2^2 < 1.5^2
    df = df.copy()
    df['ellip'] = (df['ext_shapeHSM_HsmShapeRegauss_e1'] ** 2 +
                   df['ext_shapeHSM_HsmShapeRegauss_e2'] ** 2)**0.5
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

    # from: ../data/dmstack_csv/src_lsst_mono_z1.5_000.csv
    # to  : dmstack_txt/src_lsst_mono_z1.5_000.txt
    ofile = ifile.replace('../data/dmstack_csv', 'dmstack_txt')
    ofile = ofile.replace('.csv', '.txt')
    np.savetxt(ofile,df.values,header=header_line,delimiter='\t')

def func1():
    infiles = ['../data/dmstack_csv/src_lsst_z1.5_{:03d}.csv'.format(i) for i in range(RANGE)]
    for ifile in infiles:
        file_number = int(ifile.rstrip('.csv').split('_')[-1])
        remove_nans(ifile, file_number)

def func2():
    infiles = ['../data/dmstack_csv/src_lsst90_z1.5_{:03d}.csv'.format(i) for i in range(RANGE)]
    for ifile in infiles:
        file_number = int(ifile.rstrip('.csv').split('_')[-1])
        remove_nans(ifile, file_number)

def func3():
    infiles = ['../data/dmstack_csv/src_lsst_mono_z1.5_{:03d}.csv'.format(i) for i in range(RANGE)]
    for ifile in infiles:
        file_number = int(ifile.rstrip('.csv').split('_')[-1])
        remove_nans(ifile, file_number)

def func4():
    infiles = ['../data/dmstack_csv/src_lsst_mono90_z1.5_{:03d}.csv'.format(i) for i in range(RANGE)]
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
