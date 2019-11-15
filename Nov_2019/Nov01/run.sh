#=============================================
# File Name : run.sh

# Purpose :
# 1. dmstack gives csv files
# 2. clean csv files and get txt files
# 3. use txt files and get final_text.txt using imcat
# 4. then plot gmsq

# Creation Date : Nov 01, 2019 Fri

# Last Modified :

# Created By : Bhishan Poudel 

#=============================================
echo "Estimated time: 3 min 45 seconds."
echo "Cleaning old files: catalogs, final and dmstack_txt"
rm -rf catalogs/*.cat
rm -rf final/*
rm -rf dmstack_txt/*

echo "Removing nans"
/Users/poudel/Library/Enthought/Canopy/edm/envs/deeplr/bin/python b00_remove_nans_dmstack.py

echo "Creating cat files"
bash b01_combine_four_txts_to_lc_catalog.sh

echo "Creating gmsq plot"
/Users/poudel/Library/Enthought/Canopy/edm/envs/deeplr/bin/python b02_plot_gmsq.py

