for i in {0..23}
   do
       /Users/poudel/Library/Enthought/Canopy/edm/envs/deeplr/bin/python b01_remove_nans_dmstack.py [$i] &&
        bash b02_combine_four_txts_to_lc_catalog.sh [$i]  &&
       /Users/poudel/Library/Enthought/Canopy/edm/envs/deeplr/bin/python b03_plot_gmsq.py $i
done;






