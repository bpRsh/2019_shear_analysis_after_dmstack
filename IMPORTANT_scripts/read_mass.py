
#!python
# -*- coding: utf-8 -*-#
"""
Read mass output from processCcd.py into a text file.

Author : Bhishan Poudel
Date   : Jul 13, 2018
"""
# Imports
import os
import sys

def read_mass(mass_txt):
    # 'MaxLike	1.153734e+15	2.949554e+14	6.627750e+14'
    infile = 'sim_masslin_calFalse_zphot_ref.hdf5.m200.mass.summary.txt'
    mass = 0.0
    with open(infile) as fi:
        for line in fi:
            # MaxLike	1.153734e+15	2.949554e+14	6.627750e+14
            if line.lstrip().startswith('MaxLike'):
                mass = line.split()[1]
                print("MaxLike mass = {}".format(mass))

    os.remove('sim_masslin_calFalse_zphot_ref.hdf5.chain.pkl')
    os.remove('sim_masslin_calFalse_zphot_ref.hdf5.log')
    os.remove('sim_masslin_calFalse_zphot_ref.hdf5.m200.mass.pkl')
    os.remove('sim_masslin_calFalse_zphot_ref.hdf5.m200.mass.summary.pkl')

    os.rename(infile,mass_txt)

    return mass


def main():
    mass_txt = 'mass_' + sys.argv[1][0:-5] + '.txt'
    print('Writing: ', mass_txt)
    read_mass(mass_txt)

if __name__ == "__main__":
    main() 