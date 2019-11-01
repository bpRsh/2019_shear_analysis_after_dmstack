Links:
- [a00_e1_vs_e2_plots](https://nbviewer.jupyter.org/github/bpRsh/2019_shear_analysis_after_dmstack/blob/master/Nov_2019/a00_e1_vs_e2_plots.ipynb)
- [a01_e1_e2_dmstack_params](https://nbviewer.jupyter.org/github/bpRsh/2019_shear_analysis_after_dmstack/blob/master/Nov_2019/a01_e1_e2_dmstack_params.ipynb)
- [a03_dmstack_bad_gmsq_density](https://nbviewer.jupyter.org/github/bpRsh/2019_shear_analysis_after_dmstack/blob/master/Nov_2019/a03_dmstack_bad_gmsq_density.ipynb)


# How final_text.txt was created?
```
Date: Oct 29, 2019

# Copy dmstack outputs
Copy the dmstack outputs from simplici to pisces for the jedisim simulation z=1.5 and ngals = 10k.
I have already set up password free ssh between pisces and simplici. I can simply run a bash script to copy csv files from simplic to current working directory in pisces. Running this script,
copies 400 csv files from simplici to current working directory.
```bash
bash copy_from_simplici.sh

ls *.csv | wc -l  # 400  (there are no missing files.)

# src_lsst_z1.5_000.csv to 099.csv
# src_lsst90_z1.5_000.csv to 099.csv
# src_lsst_mono_z1.5_000.csv to 099.csv
# src_lsst_mono90_z1.5_000.csv to 099.csv
```

# Remove nans from dmstack csv files, select few columns and create txt files
The output of dmstack csv files contains lots of nans. This script will choose only few parameters, does some filterings and remove the nans. From a.csv it gives a.txt file.
```bash
python remove_nans_dmstackpy
```

# Combine four text files to get lc catalog.
We now use imcat command mergecats, which will use some default tolerance to determine the
same objects in two or more lc catalogs and will merge the catalogs. From l.txt, l9.txt, m.txt, and m9.txt we get final/final_000.cat. This final_000.cat is a binary file. We combine all these
binary lc catalog files (final_000.cat to final_099.cat) to a single file final.cat and make it text file `final_text.txt`. This text file has following columns:
```bash
# fN[0][0]       fN[1][0]       fN[2][0]       fN[3][0]
# id[0][0]       id[1][0]       id[2][0]       id[3][0]
# x[0]           x[1]
# errx[0][0]     errx[0][1]     errx[1][0]     errx[1][1]
# errx[2][0]     errx[2][1]     errx[3][0]     errx[3][1]
#
# g[0][0]        g[0][1]        g[1][0]        g[1][1]
# g[2][0]        g[2][1]        g[3][0]        g[3][1]
#
# ellip[0][0]    ellip[1][0]    ellip[2][0]    ellip[3][0]
# flux[0][0]     flux[1][0]     flux[2][0]     flux[3][0]
# radius[0][0]   radius[1][0]   radius[2][0]   radius[3][0]
# gm[0]          gm[1]          gc[0]          gc[1]
```

Note that here g means ellipticity. The reduced shear is g/2.
