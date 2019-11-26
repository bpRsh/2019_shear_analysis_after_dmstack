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
