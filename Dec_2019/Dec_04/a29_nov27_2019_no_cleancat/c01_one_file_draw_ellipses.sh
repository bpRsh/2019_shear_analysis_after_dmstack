# variables
TSV="df_gmdsq_lt_bin10_file0.tsv"
CAT="df_gmdsq_lt_bin10_file0.cat"

# create lc catalog from tsv
lc -C -N '1 2 x' -N '1 2 gm' -n radius  < "${TSV}" > "${CAT}"

# draw ellipse on fitsfile using given .cat file
FITS="lsst_mono_z1.5_000.fits"

makechart -r radius 2 -e gm 1 -v 60000 -f "$FITS" < "${CAT}" > ellipse_"${FITS}"
