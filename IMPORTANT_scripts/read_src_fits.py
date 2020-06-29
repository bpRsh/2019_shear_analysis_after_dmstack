#!python
# -*- coding: utf-8 -*-#
"""
Reading fitsfile table

@author: Bhishan Poudel

@date: Feb 9, 2018

Ref: http://docs.astropy.org/en/stable/io/fits/usage/table.html

"""
# Imports
import numpy as np
from astropy.io import fits
import glob

def src_fits_table(src_fits):
    # Read table and its fields
    table = fits.open('%s' %(src_fits))
    data = table[1].data
    cols = table[1].columns
    hdrs = table[1].header
    names = data.names # names[0] is flags, 1 is id and so on.

    # Fields I need
    fields= ['deblend_nChild',
             'ext_shapeHSM_HsmPsfMoments_x',
             'ext_shapeHSM_HsmPsfMoments_y',
             'ext_shapeHSM_HsmPsfMoments_xx',
             'ext_shapeHSM_HsmPsfMoments_yy',
             'ext_shapeHSM_HsmPsfMoments_xy',
             'ext_shapeHSM_HsmShapeRegauss_e1',
             'ext_shapeHSM_HsmShapeRegauss_e2',
             'ext_shapeHSM_HsmShapeRegauss_sigma']


    # numpy array
    outdat = np.array([ data.field(fields[0]),
                       data.field(fields[1]),
                       data.field(fields[2]),
                       data.field(fields[3]),
                       data.field(fields[4]),
                       data.field(fields[5]),
                       data.field(fields[6]),
                       data.field(fields[7]),
                       data.field(fields[8])
        ]).T


    # NOTE: EXCLUDE NANs 
    # checking nChild ==0 (we take only zero values)
    #
    #
    outdat = outdat[~np.isnan(outdat).any(axis=1)]  
    nchild = outdat[:,0]
    #
    # confirm not nans
    # print("np.any(nchild!=0) = {}".format(np.any(nchild!=0)))

    # prepare to write data
    hdr_lst = ['nChild','x','y','xx','yy','xy','e1','e2','sigma']
    hdr = '       '.join(hdr_lst)
    np.savetxt('src_fits.csv',outdat,fmt='%8.4f',header=hdr)

def main():
    """Run main function."""
    src_fits = glob.glob('output/src/*/src.fits')[0]

    # Load sources and print all columns
    if src_fits=='':
        src_fits = 'src.fits'
        
    src_fits_table(src_fits)

if __name__ == "__main__":
    main()
