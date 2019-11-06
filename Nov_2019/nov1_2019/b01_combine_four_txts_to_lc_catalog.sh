# Author  : Bhishan Poudel
# Date    : July 5, 2019
# Update  : Oct 29, 2019

# Description:
#==============
# 
# Usage: bash combine_four_txts_to_lc_catalog.sh
#
# Outputs:
#=========
# Inputs : l.txt, l9.txt, m.txt, m9.txt and gives final/final_000.txt
# Main output: final/final_text.txt
# Temp output: catalogs/*.cat
#
# Detail description:
# ====================
#
# Example .txt has following columns:
#
# column 0,1   : fN     = file_number, id = id
# column 2,3   : x      = base_SdssCentroid_x, base_SdssCentroid_y
# column 4,5   : errx   = base_SdssCentroid_xSigma, base_SdssCentroid_ySigma
# column 6,7,8 : ellip  = ext_shapeHSM_HsmShapeRegauss_e1, ext_shapeHSM_HsmShapeRegauss_e2, ellip
# column 9     : flux   = base_SdssShape_flux
# column 10    : radius = 4th root of (xx*xy - xy*xy)
#
# Output File
#=========================
# fN[0][0]       fN[1][0]       fN[2][0]       fN[3][0]
# id[0][0]       id[1][0]       id[2][0]       id[3][0]
# x[0]           x[1]
# errx[0][0]     errx[0][1]     errx[1][0]     errx[1][1]
# errx[2][0]     errx[2][1]     errx[3][0]     errx[3][1]
#
# g[0][0]        g[0][1]        g[1][0]        g[1][1]
# g[2][0]        g[2][1]        g[3][0]        g[3][1]
#
# shear[0][0]    shear[1][0]    shear[2][0]    shear[3][0]
# flux[0][0]     flux[1][0]     flux[2][0]     flux[3][0]
# radius[0][0]   radius[1][0]   radius[2][0]   radius[3][0]
# gm[0]          gm[1]          gc[0]          gc[1]
#
#
#==================================================
# NOTE: I have updated the script. Now shear is ellip/2 and there  is no ellip.
#==================================================

z=1.5
BEGIN=0
END=99 # end is included

# main output folder
mkdir -p final
mkdir -p catalogs

# loop through range of files
for i in $(seq -f "%03g" $BEGIN $END)
do
    # texts
    LT="dmstack_txt/src_lsst_z${z}_${i}"
    L9T="dmstack_txt/src_lsst90_z${z}_${i}"
    MT="dmstack_txt/src_lsst_mono_z${z}_${i}"
    M9T="dmstack_txt/src_lsst_mono90_z${z}_${i}"
    
    # catalogs
    LC="catalogs/src_lsst_z${z}_${i}"
    L9C="catalogs/src_lsst90_z${z}_${i}"
    MC="catalogs/src_lsst_mono_z${z}_${i}"
    M9C="catalogs/src_lsst_mono90_z${z}_${i}"

    # create lc catalog from text file
    # in imcat we must read all columns
    # unused columns further: id flux radius
    #echo "Creating: .cat files";
    lc -C -n fN -n id -N '1 2 x' -N '1 2 errx' -N '1 2 g' -n shear -n flux -n radius < "${LT}".txt > "${LC}".cat
    lc -C -n fN -n id -N '1 2 x' -N '1 2 errx' -N '1 2 g' -n shear -n flux -n radius < "${L9T}".txt > "${L9C}".cat

    lc -C -n fN -n id -N '1 2 x' -N '1 2 errx' -N '1 2 g' -n shear -n flux -n radius < "${MT}".txt > "${MC}".cat
    lc -C -n fN -n id -N '1 2 x' -N '1 2 errx' -N '1 2 g' -n shear -n flux -n radius < "${M9T}".txt > "${M9C}".cat

    # merge the 4 catalogs to a single catalog
    # Make sure mergecats have mono files first and then chromatic files later
    # to comply with the command to create final.cat.
    #echo "Creating: merge.cat"
    mergecats 5 "${MC}".cat "${M9C}".cat "${LC}".cat "${L9C}".cat > merge.cat &&
    #echo "Created: merge.cat"

    # convert the merge catalog into a catalog with mono and color shear values with the 0 degree and 90 degree values averaged:
    #echo "Creating: final.cat";
    lc -b +all 'x = %x[0][0] %x[1][0] + %x[2][0] + %x[3][0] + 4 / %x[0][1] %x[1][1] + %x[2][1] + %x[3][1] + 4 / 2 vector' 'gm = %g[0][0] %g[1][0] + 2 / %g[0][1] %g[1][1] + 2 / 2 vector' 'gc = %g[2][0] %g[3][0] + 2 / %g[2][1] %g[3][1] + 2 / 2 vector' < merge.cat > final/final_${i}.cat

    echo "Created: final/final_${i}.cat"
done;

# combine all final catalogs
cd final;
catcats *.cat > final.cat

# convert binary to text
lc -O < final.cat > final_text.txt 

# remove temp file
rm ../merge.cat
