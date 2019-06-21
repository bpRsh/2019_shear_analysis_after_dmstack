# Remove nans from textfile output of dmstack and only extract few columns 
# Author: Bhishan Poudel
#
# Filtering:  
# 1. flag calib_psfCandidate==False
# 2. column deblend_nChild==0
# 3. ellipticity e =  sqrt(e1^2 + e2^2) < 1.5
# 4. choose only few columns given below
# 5. remove nans from all these columns
# 6. change delimiter to tab.
# 
# columns:
# id (90)
# base_SdssCentroid_x, base_SdssCentroid_y (102, 103)
# base_SdssCentroid_xSigma, base_SdssCentroid_ySigma (104,105)
# ext_shapeHSM_HsmShapeRegauss_e1, ext_shapeHSM_HsmShapeRegauss_e2 (127, 128)
# base_SdssShape_flux (114)
#
# In total there are 8 columns
# id
# x1,x2 xerr1 xerr2
# e1 e2
# flux
#
import pandas as pd
import numpy as np
import sys
import glob

def remove_nans(ifile):
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
    """

    usecols = [1, 94, 90, 102, 103, 104, 105, 127, 128, 114]
    df = pd.read_csv(ifile, sep=",",low_memory=False)

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
    df['e'] = (df['ext_shapeHSM_HsmShapeRegauss_e1'] ** 2 + df['ext_shapeHSM_HsmShapeRegauss_e2'] ** 2)**0.5

    df = df.query('e < 1.5')

    # take only required columns
    cols_select = ['id',
           'base_SdssCentroid_x', 'base_SdssCentroid_y',
           'base_SdssCentroid_xSigma','base_SdssCentroid_ySigma',
           'ext_shapeHSM_HsmShapeRegauss_e1','ext_shapeHSM_HsmShapeRegauss_e2',
           'base_SdssShape_flux']

    df = df[cols_select]

    # drop all nans
    df = df.dropna()

    # write txt file with commented header
    prefix = ' '*11
    header_line = prefix.join(cols_select)
    np.savetxt(ifile[0:-4]+'.txt',df.values,header=header_line,delimiter='\t')

if __name__ == '__main__':
    for ifile in glob.glob("*.csv"):
        print("Reading: ", ifile)
        remove_nans(ifile)
