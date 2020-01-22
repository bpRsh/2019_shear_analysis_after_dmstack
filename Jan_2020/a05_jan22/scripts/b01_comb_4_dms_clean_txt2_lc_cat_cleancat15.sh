# Author  : Bhishan Poudel
# Date    : July 5, 2019
# Update  : Dec 5, 2019

# Description
# Added gmd variable to catalog.

# Time Taken: It takes 15 seconds to read 100*4 text files in ../data/dmstack_txt
#                   ant to create catalogs/*.cat and final/*.cat
#
# Main output:  final/final_text.txt
# fixed parameters
z=1.5
CLEANCATVAL=15

# input dir
dmstack_txt="dmstack_txt" # must have N*4 files in this folder

# files I have in the input dir
BEGIN=$1 # 0
END=$2  # end is included

# outputs
final="final"
catalogs="catalogs"
mkdir -p $final
mkdir -p $catalogs

    # loop through range of files
    for i in $(seq -f "%03g" $BEGIN $END)
        do # do of 0 to N
            # texts
            LT="${dmstack_txt}/src_lsst_z${z}_${i}"
            L9T="${dmstack_txt}/src_lsst90_z${z}_${i}"
            MT="${dmstack_txt}/src_lsst_mono_z${z}_${i}"
            M9T="${dmstack_txt}/src_lsst_mono90_z${z}_${i}"

            # catalogs
            LC="${catalogs}/src_lsst_z${z}_${i}"
            L9C="${catalogs}/src_lsst90_z${z}_${i}"
            MC="${catalogs}/src_lsst_mono_z${z}_${i}"
            M9C="${catalogs}/src_lsst_mono90_z${z}_${i}"

            # create lc catalog from text file
            # in imcat we must read all columns
            # unused columns further: id flux radius
            #echo "Creating: .cat files";
            lc -C -n fN -n id -N '1 2 x' -N '1 2 errx' -N '1 2 g' -n ellip -n flux -n radius < "${LT}".txt   |  lc +all 'mag = %flux log10 -2.5 *'  |  cleancat $CLEANCATVAL  > "${LC}".cat
            lc -C -n fN -n id -N '1 2 x' -N '1 2 errx' -N '1 2 g' -n ellip -n flux -n radius < "${L9T}".txt  | lc +all 'mag = %flux log10 -2.5 *'  |  cleancat $CLEANCATVAL  > "${L9C}".cat

            lc -C -n fN -n id -N '1 2 x' -N '1 2 errx' -N '1 2 g' -n ellip -n flux -n radius < "${MT}".txt  |  lc +all 'mag = %flux log10 -2.5 *'  |  cleancat $CLEANCATVAL   >  "${MC}".cat
            lc -C -n fN -n id -N '1 2 x' -N '1 2 errx' -N '1 2 g' -n ellip -n flux -n radius < "${M9T}".txt  |  lc +all 'mag = %flux log10 -2.5 *'  |  cleancat $CLEANCATVAL  > "${M9C}".cat

            # merge the 4 catalogs to a single catalog
            # Make sure mergecats have mono files first and then chromatic files later
            # to comply with the command to create final.cat.
            mergecats 5 "${MC}".cat "${M9C}".cat "${LC}".cat "${L9C}".cat > ${catalogs}/merge.cat &&
            #echo "Created: merge.cat"

            # convert the merge catalog into a catalog with mono and color shear values with the 0 degree and 90 degree values averaged:
            #echo "Creating: final.cat";
            lc -b +all 'x = %x[0][0] %x[1][0] + %x[2][0] + %x[3][0] + 4 / %x[0][1] %x[1][1] + %x[2][1] + %x[3][1] + 4 / 2 vector' 'gm = %g[0][0] %g[1][0] + 2 / %g[0][1] %g[1][1] + 2 / 2 vector' 'gc = %g[2][0] %g[3][0] + 2 / %g[2][1] %g[3][1] + 2 / 2 vector'   'gmd = %g[0][0] %g[1][0] - 2 / %g[0][1] %g[1][1] - 2 / 2 vector' 'gcd = %g[2][0] %g[3][0] - 2 / %g[2][1] %g[3][1] - 2 / 2 vector' < ${catalogs}/merge.cat > ${final}/final_${i}.cat

        done; # done of 0 to N

        # combine all final catalogs
        cd $final;
        catcats *.cat > final.cat

        # convert binary to text
        lc -O < final.cat > final_text.txt

        # go back to original dir
        cd -

## command: bash a01_comb_4_dms_clean_txt2_lc_cat_cleancat15.sh 100 150
## command: bash a01_comb_4_dms_clean_txt2_lc_cat_cleancat15.sh 151 200