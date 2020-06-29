#!python
# -*- coding: utf-8 -*-#
"""
Create yaml file.

Author : Bhishan Poudel
Date   : Jul 13, 2018
"""
# Imports 
import os

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


if __name__ == "__main__":

    # mass estimation variables
    sim_yaml = 'sim.yaml'  # butler file
    sim_txt = 'sim.txt'  # galaxy_parent redshift

    ra = 0.1
    dec = 0.1
    z_lens = 0.3
    yaml_create(sim_yaml,sim_txt,ra,dec,z_lens)

"""
Command: python yaml_create.py

"""