#!python
# -*- coding: utf-8 -*-#
#
# Author      : Bhishan Poudel; Physics Graduate Student, Ohio University
# Date        : July 26, 2017
# Last update : Mar 11, 2019

'''

This program adds the PSF stars to all the lsst, lsst90, lsst_mono and lsst_mono90 fitsfiles from the PSF files from another directory (e.g. stars_z0.7_100_100000)

This program does not create star files, it just combines stars to the jedisim
output galaxies.

# Required:
# 1. Inside idir:  lsst,lsst90,lsst_mono and lsst_mono90 
# 2. At pwd:  stars_z{z}_{nstar}_{starval}
#    Inside that: star{b,d,m}_z{z}_{nstar}_{starval}.fits
#
#                                 z   idir              nstar starval
# Command: python add_wcs_star.py 0.7 jout_z0.7_000_099 100 100000 
#
# Outputs: wcs_star_$idir   with star and wcs added to input fitsfiles.
#
# Time: Takes about 12 minutes for 100 files.

'''


#
# Imports
from __future__ import print_function, unicode_literals, division, absolute_import, with_statement
from astropy.cosmology import FlatLambdaCDM
import glob
import os
import numpy as np
from astropy.io import fits
from astropy import wcs
import sys

def add_wcs(field):
    # Read field
    field = str(field)
    field_hdu = fits.open(field)

    # Get fake wcs from astropy
    w = wcs.WCS(naxis=2)
    w.wcs.crpix = [1800.0, 1800.0]
    w.wcs.crval = [0.1, 0.1]
    w.wcs.cdelt = np.array([-5.55555555555556E-05,5.55555555555556E-05])
    w.wcs.ctype = ["RA---TAN", "DEC--TAN"]
    wcs_hdr = w.to_header()

    # Add fake wcs to header of output file
    hdr = field_hdu[0].header
    hdr += wcs_hdr

    # Write output file
    field_hdu.writeto(field,overwrite=True)
    field_hdu.close()

    # Print
    print('Fake WCS added to the galaxy field: {}'.format(field))

def main():
    """Run main function."""
    z = sys.argv[1] # 0.5
    idir = sys.argv[2] # jout_z0.5_000_099 (inside this
                       #   we must have lsst, lsst_mono and 90s.
    nstar = sys.argv[3]
    starval = sys.argv[4]

    mono = ['lsst_mono','lsst_mono90']
    chro = ['lsst','lsst90']

    mono = ['{}/{}/'.format(idir,f) for f in mono]
    chro = ['{}/{}/'.format(idir,f) for f in chro]

    # star data
    dat_stars = [fits.getdata('stars_z{}_{}_{}/star{}_z{}_{}_{}.fits'.format(z,nstar,
                      starval, i,z,nstar,starval)) for i in list('bdm')]

    # create output dirs
    odirs = ['wcs_star_{}'.format(o) for o in mono+chro]
    for o in odirs:
        if not os.path.isdir(o):
            os.makedirs(o)

    # mono
    for m in mono:
        for f in glob.glob('{}/*.fits'.format(m)):
            datm = fits.getdata(f)
            odat = datm + dat_stars[2] # mono + starm
            head, tail = os.path.split(f)
            ofile = 'wcs_star_' + head + '/' + tail
            print('\nWriting: ', ofile)
            fits.writeto(ofile,odat,overwrite=True)
            add_wcs(ofile)

    # chro
    for c in chro:
        for f in glob.glob('{}/*.fits'.format(c)):
            datc = fits.getdata(f)
            odat = datc + dat_stars[0] + dat_stars[1] # chro + starb + stard
            head, tail = os.path.split(f)
            ofile = 'wcs_star_' + head + '/' + tail
            print('\nWriting: ', ofile)
            fits.writeto(ofile,odat,overwrite=True)
            add_wcs(ofile)


if __name__ == "__main__":
    main()

# Required: 
# 1. Inside idir: lsst,lsst90,lsst_mono and lsst_mono90
# 2. Inside  stars_z{z}_{nstar}_{starval}:
#                star{b,d,m}_z{z}_{nstar}_{starval}.fits
#
#                                 z   idir            nstar starval
# Command: python add_wcs_star.py 0.7 jout_z0.7_000_099 100 100000 
#
# Outputs: wcs_star_$idir   with star and wcs added to input fitsfiles.
# Run time: z=0.7 0-999 files, Sep 26, 2018 it took me 11 minutes.

