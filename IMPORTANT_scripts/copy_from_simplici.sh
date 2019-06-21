#!/usr/bin/env sh

######################################################################
# @author      : poudel (poudel@$HOSTNAME)
# @file        : copy_from_simplici
# @created     : Thursday Jun 13, 2019 15:24:04 EDT
#
# @description : Copy files from simplici 
######################################################################
z=1.5

#BEGIN=0
BEGIN=5  # for ngals20k I have started from 5
END=99 #last is also included

for n in $( seq -f "%03g" $BEGIN $END )
do
        LSST="lsst"
        DATE="2019_04_30_17_24_ngals20k"
        DM="~/Rsh_out/z$z/wcs_star_jout_z"$z"_"$DATE"/"$LSST"/dmstack_output/"
        TXT="dm_out_z"$z"_"$LSST"/txt_"$LSST"_z"$z"/src_"$LSST"_z"$z"_"$n".csv"
        FILE1="$DM""$TXT"

        FILE2=${FILE1//lsst/lsst90}
        FILE3=${FILE1//lsst/lsst_mono}
        FILE4=${FILE1//lsst/lsst_mono90}

        # debug
        # ~/Rsh_out/z1.5/wcs_star_jout_z1.5_2019_04_30_17_24_ngals20k/lsst/dmstack_output/dm_out_z1.5_lsst/txt_lsst_z1.5/src_lsst_z1.5_001.csv
        #echo "$FILE1"

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
                DM="~/Rsh_out/z$z/wcs_star_jout_z"$z"_"$DATE"/"$LSST"/dmstack_output/"
                TXT="dm_out_z"$z"_"$LSST"/txt_"$LSST"_z"$z"/src_"$LSST"_z"$z"_"$n".csv"
                FILE="$DM""$TXT"
                scp -r poudel@simplici.phy.ohio.edu:"$FILE" .
            done;
        else
            echo "$n" " $LSST"  does not exist.
        fi;
done;
