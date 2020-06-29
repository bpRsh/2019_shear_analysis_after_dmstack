#!python
# -*- coding: utf-8 -*-#
"""
Pyhton script to run dmstack commands for mass estimation of a cluster.

@author: Bhishan Poudel

@date: Mar 30, 2018

:Command: python aa_run_dmstack.py -z 0.7

:Shell commands: mkdir, mv

:Depends:

 aa_processCcdConfig.py
 aa_run_dmstack.py

"""
# Imports
import os,sys,argparse
import time
import glob
import shutil
import numpy as np
import pyfits
import astropy.table as table
from astropy.io import fits

def src_fits_table(jedi_file,src_txt):
    src_folder = jedi_file.split('.')[0]
    src_fits = 'output/src/{}/src.fits'.format(src_folder)

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
    print('Creating: {}'.format(src_txt))
    np.savetxt(src_txt,outdat,fmt='%8.4f',header=hdr)

def create_hdf5_simtxt(jedi_file,sim_hdf5,sim_txt,z_sim):
    src_fits = 'output/src/{}/src.fits'.format(jedi_file.split('.')[0])

    print('Reading: {}'.format(src_fits))
    cat_sim = pyfits.open(src_fits)
    ra_pix = cat_sim[1].data['base_GaussianCentroid_X']
    dec_pix = cat_sim[1].data['base_GaussianCentroid_y']
    ra = np.abs(ra_pix*0.2/3600.-0.2) # assumes a 0.2 arcmin pixel size
    dec = dec_pix*0.2/3600.

    e1 = cat_sim[1].data['ext_shapeHSM_HsmShapeRegauss_e1']
    e2 = cat_sim[1].data['ext_shapeHSM_HsmShapeRegauss_e2']
    obj_id = cat_sim[1].data['id']

    # Write pipeline-compatible hdf5 file
    deepCoadd_meas = table.Table([obj_id, ra, dec, e1, e2], names=('id', 'coord_ra_deg', 'coord_dec_deg', 'ext_shapeHSM_HsmShapeRegauss_e1', 'ext_shapeHSM_HsmShapeRegauss_e2'))
    print('Writing: {}'.format(sim_hdf5))
    deepCoadd_meas.write(sim_hdf5, path='deepCoadd_meas', overwrite=True)

    zsim_data = np.zeros(len(ra))+z_sim
    data = np.array([obj_id, zsim_data])

    print('Writing: ', sim_txt)

    np.savetxt(sim_txt, data.T, fmt=['%i','%f'])


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



def yaml_create(sim_yaml,sim_txt,ra,dec,z_lens):
    """Create sim.yaml file."""
    output = os.getcwd() + '/output'
    sim_yaml_data = """
{
"cluster": "SIM_cluster",
"ra": %f,
"dec": %f,
"redshift": %f,
"filter": ["u", "g", "r", "i", "i2", "z"],
"butler": "%s",
"keys": {'src':["id", "coord*", "ext_shapeHSM_HsmSourceMoments_x", "ext_shapeHSM_HsmSourceMoments_y", "ext_shapeHSM_HsmShapeRegauss_e1", "ext_shapeHSM_HsmShapeRegauss_e2"]},
"sim": {"flag" : True, "zfile":"%s"},
"mass":{ "zconfig" : "zphot_ref",
         "mprior":'lin'}
}"""% (ra,dec,z_lens,output,sim_txt)

    with open(sim_yaml,'w') as fo:
        fo.write(sim_yaml_data.lstrip())

def create_src_fits(jedi_file,noise):
    mymap='mkdir -p input && echo "lsst.obs.file.FileMapper" > input/_mapper'
    ingest='ingestImages.py input/ {} --mode link'.format(jedi_file)
    prccd='processCcd.py input/ --id filename={} --config isr.noise={} --configfile aa_processCcdConfig.py --clobber-config --output output'.format(jedi_file,noise)

    os.system(mymap)
    os.system(ingest)
    os.system(prccd)

def mass_estimation(jedi_file,sim_yaml,sim_hdf5,sim_txt, ra,dec,z_lens,z_sim):
    yaml_create(sim_yaml,sim_txt,ra,dec,z_lens)
    create_hdf5_simtxt(jedi_file,sim_hdf5,sim_txt,z_sim)

    # Add zpho references to sim.hdf5
    zphot='clusters_zphot.py sim.yaml sim.hdf5'
    os.system(zphot)

    # estimate the max likelihood of mass
    mass='clusters_mass.py {} {}'.format(sim_yaml,sim_hdf5)
    os.system(mass)

def main(z_sim,fname):
    """Run main function.

    z_sim: redshift e.g. 0.7
    fname : lsst or lsst90 or lsst_mono or lsst_mono90

    """

    # obs_file variables
    src_txt = 'src.txt' # output of obs_file
    noise = 5

    # mass estimation variables
    sim_yaml = 'sim.yaml'  # butler file
    sim_hdf5 = 'sim.hdf5' # hdf5 file with some fields
    sim_txt = 'sim.txt'  # galaxy_parent redshift
    mass_txt = 'mass.txt'
    ra = 0.1
    dec = 0.1
    z_lens = 0.3

    # Copy outputs
    tm   = time.strftime("%Y_%m_%d_%H_%M")
    odir = 'dmstack_output/z{}_{}/dm_out_{}_z{}'.format(z_sim,tm,fname,z_sim)
    if not os.path.isdir(odir):
        os.makedirs(odir)

    # create mass,txt,fits folders inside odir
    dmo_fits = odir + '/fits_{}_z{}'.format(fname,z_sim)
    dmo_txt  = odir + '/txt_{}_z{}'.format(fname,z_sim)
    dmo_mass = odir + '/mass_{}_z{}'.format(fname,z_sim)
    os.makedirs(dmo_fits)
    os.makedirs(dmo_txt)
    os.makedirs(dmo_mass)

    # Write output names in dropbox textfile.
    drop_odir = os.path.expanduser("~") + '/Dropbox/dmout'
    if not os.path.isdir(drop_odir):
        os.makedirs(drop_odir)
    drop_otxt =  '{}/dmout_{}_z{}_{}.txt'.format(drop_odir,fname,z_sim,tm)

    # Create empty textfile in dropbox to be added later.
    print('Creating: {}'.format(drop_otxt))
    with open(drop_otxt,'w') as fo:
        fo.write("")


    for jedi_file in glob.glob('*.fits'):

        # try to run dmstack, some of the files may fail
        try:

            # Time for Dropbox
            loop_start_time = time.time()


            # remove input and output
            if os.path.isdir('input'):
                shutil.rmtree('input')

            if os.path.isdir('output'):
                shutil.rmtree('output')

            # backup old txt files
            os.system('mkdir -p old_files; mv *.txt old_files/; rm -rf *.pkl *.log;')

            # obs_file
            create_src_fits(jedi_file,noise) # gives output/src/HEAD/src.fits
            src_fits_table(jedi_file,src_txt) # gives src.txt

            # clusters we get 3 pkl files, one log, and one txt file.
            mass_estimation(jedi_file,sim_yaml,sim_hdf5,sim_txt, ra,dec,z_lens,z_sim)
            read_mass(mass_txt) # rename massfile to mass.txt and delete log and pkl

            # output file name prefix
            src_fits = 'output/src/{}/src.fits'.format(jedi_file.split('.')[0])

            # Before moving pad 00 to the galaxy number
            # lsst_z0.7_0.fits
            last = jedi_file.split('_')[-1] # 0.fits
            num = last.strip('.fits') # 0
            num00 = '{:03d}'.format(int(num)) # 000
            last00 = last.replace(num,num00) # 000.fits
            jedi00 = jedi_file.replace(last,last00) # lsst_z0.7_000.fits

            # move files
            # FNAME = lsst
            #
            # From: output/src/{}/src.fits
            # To  : dmstack_output/z0.7_TIME/dm_out_lsst_z0.7/fits_lsst_z0.7/src_lsst_z0.7_0.fits
            #
            # From: 'src.txt'
            # To  : dmstack_output/z0.7_TIME/dm_out_lsst_z0.7/txt_lsst_z0.7/src_lsst_z0.7_0.txt
            #
            # From: 'mass.txt'
            # To  : dmstack_output/z0.7_TIME/dm_out_lsst_z0.7/mass_lsst_z0.7/mass_lsst_z0.7_0.txt
            #
            os.rename(src_fits, dmo_fits + '/src_' + jedi00.strip('.fits') + '.fits')
            os.rename(src_txt,  dmo_txt  + '/src_' + jedi00.strip('.fits') + '.txt')
            os.rename(mass_txt, dmo_mass + '/mass_'+ jedi00.strip('.fits') + '.txt')

            # remove input and output
            shutil.rmtree('input')
            shutil.rmtree('output')

            # Write output info in Dropbox
            loop_end_time = time.time()
            loop_time =  loop_end_time - loop_start_time

            loop_mins = loop_time / 60
            date = time.strftime("%b%d %H:%M")
            with open(drop_otxt,'a') as fo:
                fo.write('{} {}: z = {:.1f} Runtime {:.0f} mins and End: {}\n\n'.format(fname, num, z_sim, loop_mins, date))

        except:
            erf = 'ERRRORS.txt'
            drop_erf = '{}/{}_{}'.format(drop_odir,fname,erf)
            with open(erf,'a') as fo, open (drop_erf, 'a') as fo2 :
                fo.write('\nDMStack failed for: {}'.format(jedi_file))
                fo2.write('\nDMStack failed for: {}'.format(jedi_file))


if __name__ == "__main__":
        import time, os
        import argparse

        parser = argparse.ArgumentParser()
        parser.add_argument("-m", "--manual", help='python aa_run_dmstack.py -z 0.7 -f lsst',required=False,type=str)
        parser.add_argument("-z", "--sim_redshift", help='Redshift of the jedisim simulation',required=True,type=float)
        parser.add_argument("-f", "--fname", help='lsst or lsst90 or lsst_mono or lsst_mono90',required=True,type=str)
        args = parser.parse_args()
        z_sim = args.sim_redshift
        fname = args.fname

        # Beginning time
        program_begin_time = time.time()
        begin_ctime        = time.ctime()

        #  Run the main program
        main(z_sim,fname)

        # Print the time taken
        program_end_time = time.time()
        end_ctime        = time.ctime()
        seconds          = program_end_time - program_begin_time
        m, s             = divmod(seconds, 60)
        h, m             = divmod(m, 60)
        d, h             = divmod(h, 24)
        print("\n\nBegin time: ", begin_ctime)
        print("End   time: ", end_ctime, "\n")
        print("Time taken: {0: .0f} days, {1: .0f} hours, \
              {2: .0f} minutes, {3: f} seconds.".format(d, h, m, s))
        print("End of Program: {}".format(os.path.basename(__file__)))
        print("\n")


"""
Installation Instructions:
# First install dmstack13 using conda: https://pipelines.lsst.io/v/13-0/install/conda.html
1) conda update -n base conda
2) conda config --add channels http://conda.lsst.codes/stack/0.13.0
3) conda create --name lsst python=2
4) source activate lsst
5) conda install lsst-distrib
6) source eups-setups.sh
7) setup lsst_distrib

# Now we can use lsst environment
1) source activate lsst
2) source eups-setups.sh
3) setup lsst_distrib
4) cd ~/Softwares/obs_file
5) setup -k -r .
6) scons
7) cd -

# From obs_file we get: src.fits inside output directory.
# To get mass estimation from src.fits, we need to install Clusters.
# NOTE: before installing Clusters, install Atom (it installs Xcode) and gfortran.
#
1) cd ~/Clusters
2) pip install -r requirements.txt
3) cd ../
4) pip install Clusters/
5) cd -


Simpler method:
============= source bash_dmstack.sh =============
alias sbdm='source bash_dmstack.sh'
alias lsst='source activate lsst && source eups-setups.sh && setup lsst_distrib'
alias obs='cd ~/Softwares/obs_file && setup -k -r . && scons && cd -'

alias rmio='rm -rf input output'
alias map='mkdir -p input && echo "lsst.obs.file.FileMapper" > input/_mapper' # creates mapper
alias ingest='ingestImages.py input/ trial00.fits --mode link'  # input: registry.sqlite3 and raw/trial00.fits
alias crccd='echo "config.charImage.repair.cosmicray.nCrPixelMax=1000000" > processCcdConfig.py'
alias prccd='processCcd.py input/ --id filename=trial00.fits --config isr.noise=5 --configfile processCcdConfig.py --clobber-config --output output'
alias src='python read_src_fits.py && head src_fits.csv'

#===============================================================================
# Clusters Usage (filename: trial00.fits)
##==============================================================================
# 0) python yaml_create.py # create sim.yaml
# 1) python clusters_hdf5_simtxt.py # Create sim.txt and sim.hdf5
# 2) clusters_zphot.py sim.yaml sim.hdf5  # Adding zphot_ref  to sim.hdf5
# 3) clusters_mass.py sim.yaml sim.hdf5
#
alias yml='python yaml_create.py'
alias h5='python clusters_hdf5_simtxt.py'
alias zphot='clusters_zphot.py sim.yaml sim.hdf5' # Add zphot_ref  to sim.hdf5
alias mass='clusters_mass.py sim.yaml sim.hdf5'


USAGE: This program will get mass of all the fitsfiles in pwd.
NOTE:  The fitsfile must have psf stars and wcs information.

cd to the directory with fitsfiles whose mass is to be found
cpdm
lsst
obs
clear    # before copy the line after, then clear, and paste that command
         python aa_run_dmstack.py -z 0.7 -f lsst_OR_lsst90_etc > /dev/null 2>&1

NOTE: We can run dmstack for lsst, lsst90, lsst_mono, and lsst_mono90 in
      FOUR different terminals at the same time.

"""
