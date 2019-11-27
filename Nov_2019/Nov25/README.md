
|  Notebook | Rendered   | Description  |  Author |
|---|---|---|---|
| a01_gmdsq_larger_than_bin10_file0.ipynb  | [ipynb](https://github.com/bpRsh/2019_shear_analysis_after_dmstack/blob/master/Nov_2019/Nov25/a01_gmdsq_larger_than_bin10_file0.ipynb), [rendered](https://nbviewer.jupyter.org/github/bpRsh/2019_shear_analysis_after_dmstack/blob/master/Nov_2019/Nov25/a01_gmdsq_larger_than_bin10_file0.ipynb)  |   | [Bhishan Poudel](https://bhishanpdl.github.io/)  |



# IMCAT command
```bash
# variables 
TSV="df_gmdsq_larger_bin10_file0.tsv"
CAT="df_gmdsq_larger_bin10_file0.cat"
echo "$TSV"

# create lc catalog from tsv
echo "Creating: .cat files";
lc -C -N '1 2 x' -N '1 2 gm'   < "${TSV}" > "${CAT}"

# draw ellipse on fitsfile using given .cat file
FITS="lsst_mono_z1.5_000.fits"
echo "Creating: fitsfile with ellipse drawn on it:  ellipse_${FITS}";
makechart  -e gm 1 -v 60000 -f "$FITS" < "${CAT}" > ellipse_"${FITS}"
```

# File mono0
```python

# read imcat output file created after merging 100*4 files
file_path = f'../data/final/final_text.txt'
df = pd.read_csv(file_path,comment='#',engine='python',sep=r'\s\s+',
                 header=None,names=names)

# take all points where gmdsq > 0.399
df_gmdsq_larger_bin10 = df[df.gmdsq > bins[10]]

# add radius for mono
df_gmdsq_larger_bin10_file0['radius_mono'] = \
(df_gmdsq_larger_bin10_file0['radius[0][0]'] + 
 df_gmdsq_larger_bin10_file0['radius[1][0]'] ) /2.0
 
 df_gmdsq_larger_bin10_file0[['x[0]','x[1]','gm[0]','gm[1]','radius_mono']]\
.to_csv('df_gmdsq_larger_bin10_file0.tsv',sep='\t',header=False,index=False)

```
