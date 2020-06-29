import pyfits
import astropy.table as table
import numpy as np



srcfile = 'output/src/trial00/src.fits'
catfile = 'sim.hdf5'  # to be used with "clusters_mass.py config.yaml cat_wtg.hdf5"

print('Reading: {}'.format(srcfile))
cat_sim = pyfits.open(srcfile)
ra_pix = cat_sim[1].data['base_GaussianCentroid_X']
dec_pix = cat_sim[1].data['base_GaussianCentroid_y']
ra = np.abs(ra_pix*0.2/3600.-0.2) # assumes a 0.2 arcmin pixel size
dec = dec_pix*0.2/3600.

e1 = cat_sim[1].data['ext_shapeHSM_HsmShapeRegauss_e1']
e2 = cat_sim[1].data['ext_shapeHSM_HsmShapeRegauss_e2']
obj_id = cat_sim[1].data['id']

# Write pipeline-compatible hdf5 file
deepCoadd_meas = table.Table([obj_id, ra, dec, e1, e2], names=('id', 'coord_ra_deg', 'coord_dec_deg', 'ext_shapeHSM_HsmShapeRegauss_e1', 'ext_shapeHSM_HsmShapeRegauss_e2'))
print('Writing: {}'.format(catfile))
deepCoadd_meas.write(catfile, path='deepCoadd_meas', overwrite=True)

zsim = np.zeros(len(ra))+1.5
data = np.array([obj_id, zsim])

print('Writing: sim.txt')
np.savetxt('sim.txt', data.T, fmt=['%i','%f'])
