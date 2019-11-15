#!/usr/bin/env sh

######################################################################
# @author      : Bhishan Poudel 
# @file        : copy_from_simplici
# @created     : Thursday Jun 13, 2019 15:24:04 EDT
# @updated     : Tuesday Oct 29, 2019
#
# @description :
#
#  Copy the dmstack output csv files for lsst, lsst90, mono, mono90
#  from computer simplici to the present working directory at
#  computer pisces.
#
# Usage: 
# cd my_dmstack_analysis # or any name
# bash copy_from_simplici.sh
#
# Outputs:
# This copies lots of csv files to current directory.
# These csv files are created from dmstack and contains lots of nans.
#
# For example, this script copies csv files for z=1.5 and ngals=10k
# jedisim parameters. There are 100 * 4 csv files.
######################################################################
z=1.5
BEGIN=0
END=99 #last is also included

for n in $( seq -f "%03g" $BEGIN $END )
do
        LSST="lsst"
        DM="~/Rsh_out/z$z/wcs_star_jout_z"$z"_2019_05_15_17_00_ngals_10k/"$LSST"/dmstack_output/"
        TXT="dm_out_z"$z"_"$LSST"/txt_"$LSST"_z"$z"/src_"$LSST"_z"$z"_"$n".csv"
        FILE1="$DM""$TXT"

        FILE2=${FILE1//lsst/lsst90}
        FILE3=${FILE1//lsst/lsst_mono}
        FILE4=${FILE1//lsst/lsst_mono90}

        # check if all 4 files exist
        success=0
        ssh poudel@simplici.phy.ohio.edu "[ -f $FILE1  ]" && success=1
        ssh poudel@simplici.phy.ohio.edu "[ -f $FILE2  ]" && success=1
        ssh poudel@simplici.phy.ohio.edu "[ -f $FILE3  ]" && success=1
        ssh poudel@simplici.phy.ohio.edu "[ -f $FILE4  ]" && success=1
            
        # run only if all 4 files exist
        if ((success))
        then
            for LSST in lsst lsst90 lsst_mono lsst_mono90
            do
                DM="~/Rsh_out/z$z/wcs_star_jout_z"$z"_2019_05_15_17_00_ngals_10k/"$LSST"/dmstack_output/"
                TXT="dm_out_z"$z"_"$LSST"/txt_"$LSST"_z"$z"/src_"$LSST"_z"$z"_"$n".csv"
                FILE="$DM""$TXT"
                scp -r poudel@simplici.phy.ohio.edu:"$FILE" .
            done;
        else
            echo "$n" " $LSST"  does not exist.
        fi;
done;
