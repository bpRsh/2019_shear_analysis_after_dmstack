# Added cleancat filterings


|  Notebook | Rendered   | Description  |  Author |
|---|---|---|---|
| cleancat15  | [ipynb](https://github.com/bpRsh/2019_shear_analysis_after_dmstack/blob/master/Dec_2019/Dec_04/a29_nov27_2019_cleancat15/b03_gmdsq_larger_than_bin10_file0.ipynb), [rendered](https://nbviewer.jupyter.org/github/bpRsh/2019_shear_analysis_after_dmstack/blob/master/Dec_2019/Dec_04/a29_nov27_2019_cleancat15/b03_gmdsq_larger_than_bin10_file0.ipynb)  |   | [Bhishan Poudel](https://bhishanpdl.github.io/)  |
| cleancat20  | [ipynb](https://github.com/bpRsh/2019_shear_analysis_after_dmstack/blob/master/Dec_2019/Dec_04/a29_nov27_2019_cleancat20/b03_gmdsq_larger_than_bin10_file0.ipynb), [rendered](https://nbviewer.jupyter.org/github/bpRsh/2019_shear_analysis_after_dmstack/blob/master/Dec_2019/Dec_04/a29_nov27_2019_cleancat20/b03_gmdsq_larger_than_bin10_file0.ipynb)  |   | [Bhishan Poudel](https://bhishanpdl.github.io/)  |
| cleancat25  | [ipynb](https://github.com/bpRsh/2019_shear_analysis_after_dmstack/blob/master/Dec_2019/Dec_04/a29_nov27_2019_cleancat25/b03_gmdsq_larger_than_bin10_file0.ipynb), [rendered](https://nbviewer.jupyter.org/github/bpRsh/2019_shear_analysis_after_dmstack/blob/master/Dec_2019/Dec_04/a29_nov27_2019_cleancat25/b03_gmdsq_larger_than_bin10_file0.ipynb)  |   | [Bhishan Poudel](https://bhishanpdl.github.io/)  |
| cleancat30  | [ipynb](https://github.com/bpRsh/2019_shear_analysis_after_dmstack/blob/master/Dec_2019/Dec_04/a29_nov27_2019_cleancat30/b03_gmdsq_larger_than_bin10_file0.ipynb), [rendered](https://nbviewer.jupyter.org/github/bpRsh/2019_shear_analysis_after_dmstack/blob/master/Dec_2019/Dec_04/a29_nov27_2019_cleancat30/b03_gmdsq_larger_than_bin10_file0.ipynb)  |   | [Bhishan Poudel](https://bhishanpdl.github.io/)  |
| nocleancat  | [ipynb](https://github.com/bpRsh/2019_shear_analysis_after_dmstack/blob/master/Dec_2019/Dec_04/a29_nov27_2019_no_cleancat/b03_gmdsq_larger_than_bin10_file0.ipynb), [rendered](https://nbviewer.jupyter.org/github/bpRsh/2019_shear_analysis_after_dmstack/blob/master/Dec_2019/Dec_04/a29_nov27_2019_no_cleancat/b03_gmdsq_larger_than_bin10_file0.ipynb)  |   | [Bhishan Poudel](https://bhishanpdl.github.io/)  |

# Filterings
```python
Usual Filtering

df = df.query('calib_psfCandidate == 0.0')
df = df.query('deblend_nChild == 0.0')
df['ellip'] = np.hypot( df['ext_shapeHSM_HsmShapeRegauss_e1'] ,
                        df['ext_shapeHSM_HsmShapeRegauss_e2'] )
df = df.query('ellip < 2.0') # it was 1.5 before

#select only few columns after filtering:
cols_select = ['base_SdssCentroid_x', 'base_SdssCentroid_y',
                'base_SdssCentroid_xSigma','base_SdssCentroid_ySigma',
                'ext_shapeHSM_HsmShapeRegauss_e1','ext_shapeHSM_HsmShapeRegauss_e2',
                'base_SdssShape_flux']
df = df[cols_select]        

# drop all nans
df = df.dropna()

# additional columns
df['radius'] =  df.eval(""" ( (ext_shapeHSM_HsmSourceMoments_xx *  ext_shapeHSM_HsmSourceMoments_yy) \
                                          -  (ext_shapeHSM_HsmSourceMoments_xy**2 ) )**0.25 """)
Shape filtering
https://github.com/LSSTDESC/DC2-analysis/blob/master/tutorials/object_gcr_2_lensing_cuts.ipynb

df = df.query('ext_shapeHSM_HsmShapeRegauss_resolution >= 0.3')
df = df.query('ext_shapeHSM_HsmShapeRegauss_sigma <= 0.4')
df = df.query('ext_shapeHSM_HsmShapeRegauss_flag== 0.0')
Filter strongly lensed objects

Take the objects with centroids >154 pixels (remove strong lens objects).
# exclude strong lens objects <=154 distance
# The shape of lsst.fits file is 3998,3998 and center is 1699,1699.
df['x_center'] = 1699
df['y_center'] = 1699
df['distance'] = ( (df['x[0]'] - df['x_center'])**2 + (df['x[1]'] - df['y_center'])**2 )**0.5
df = df[df.distance > 154]
Imcat script

# create new columns and cleaning (four files)
lc -C -n fN -n id -N '1 2 x' -N '1 2 errx' -N '1 2 g' -n ellip -n flux -n radius < "${M9T}".txt  |  lc +all 'mag = %flux log10 -2.5 *'  |  cleancat 20  |  lc +all -r 'mag' > "${M9C}".cat


# merge 4 catalogs
mergecats 5 "${MC}".cat "${M9C}".cat "${LC}".cat "${L9C}".cat > ${catalogs}/merge.cat &&


lc -b +all 
'x = %x[0][0] %x[1][0] + %x[2][0] + %x[3][0] + 4 / %x[0][1] %x[1][1] + %x[2][1] + %x[3][1] + 4 / 2 vector'
'gm = %g[0][0] %g[1][0] + 2 / %g[0][1] %g[1][1] + 2 / 2 vector' 
'gc = %g[2][0] %g[3][0] + 2 / %g[2][1] %g[3][1] + 2 / 2 vector'   
'gmd = %g[0][0] %g[1][0] - 2 / %g[0][1] %g[1][1] - 2 / 2 vector' 
'gcd = %g[2][0] %g[3][0] - 2 / %g[2][1] %g[3][1] - 2 / 2 vector' 
< ${catalogs}/merge.cat > ${final}/final_${i}.cat
```





