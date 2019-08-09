

# Introduction
1. In jedisim we used ngals = 10k, z = 1.5 and did 100 simulations. jedisim gives l,l9,m,m9 for each 100 simulations respectively for lsst, lsst90, monochormatic and monochromatic90 cases. In jedisim we have total 100*4 = 400 fits files.

2. From jedisim we get l.fits file and from this file using dmstack we get l.csv file. From 400 jedisim output fitsfiles, we get 400 dmstack output csv files. Each dmstack output csv file has 90 flags and 76 parameters, i.e. in total it has 90+76 = 166 columns such as fluxes, ellipticities and so on.

3. After dmstack we clean and filter l.csv to get l.txt which have no nans, e <= 1.5,
   is not a psf candidate and have no child.
   This file has only few columns: FileNumber(fN), id, x-y, errx-erry, e1-e2, sdssFlux.
   
4. We use these four l.txt, l9.txt, m.txt, m9.txt file in IMCAT and get final0.cat and combine 100 finalXX.cat files to get final.cat.

5. This lc catalog file final.cat (or its text conversion final_text.txt) has more columns than single final0.cat.
   ```
   fN    00 10 20 30  # fN means file number
   id    00 10 20 30
   flux  00 10 20 30

   x  0 1
   gm 0 1
   gc 0 1
   
   errx 00 01 10 11 20 21 30 31
   g    00 01 10 11 20 21 30 31 # there is no erry here in imcat output
   
   So, in total there are
   3 * 4 + 3 * 2 + 2 * 8 = 8 + 6 + 16 = 34 columns in final.cat file.
   ```
    
# June 18, 2019 Tue
```
Notebook: flux_median_low_high_shear_comparison.ipynb
purpose: compare shear below and above the median of flux (i.e. two flux bins)
result: gm_low/gm_high = 1.22 and for gc_low/gc_high = 1.21
further work: the ratio is high, create more bins of flux and find mean shears in those bins.
```

# June 20, 2019 Thu
```
Notebook: compare_shears_for_different_flux_bins.ipynb
purpose: compare shears in multiple bins of flux

task:
-----
Here, I have a big file final_text.txt which has about 200k (rows i.e. objects obtained from dmstack).
I sorted the data according to the flux and binned it into 60 bins so that each bins roughly have equal number of objects.
I found that middle bins (bins 24,25,26 etc) have more objects in the range 0.7 < gm_sq < 1.0.
I need to figure out why the object density is high in that regions. Next time I will look at each files (100 files)
and look at the  distribution of gm_sq in each files.

```

# July 16, 2019 Tue
- Notebook link (may be slow) : https://github.com/bpRsh/2019_shear_analysis_after_dmstack/blob/master/june18_2019/july15_compare_shears_each_file.ipynb

- Interactive link: https://nbviewer.jupyter.org/github/bpRsh/2019_shear_analysis_after_dmstack/blob/master/june18_2019/july15_compare_shears_each_file.ipynb

```
Notebook: july15_compare_shears_each_file.ipynb

Done:
----
I looked at 100 files (combination of l.csv, l9.csv, m.csv,m9.csv) and plotted the number of objects in the range 0.7 < gm_sq < 1.0.
Most of the files have 180 objects in this range. 16 files have more than 200 objects that have reduced shear between 0.7 < gm_sq < 1.0.

```

# July 19, 2019 Fri
- Notebook link (may be slow) : https://github.com/bpRsh/2019_shear_analysis_after_dmstack/blob/master/june18_2019/july17_bad_density_of_100_lsst_files.ipynb

- Interactive link: https://nbviewer.jupyter.org/github/bpRsh/2019_shear_analysis_after_dmstack/blob/master/june18_2019/july17_bad_density_of_100_lsst_files.ipynb

```
Notebook: july17_bad_density_of_100_lsst_files.ipynb

Done:
----
I am mostly concerned in the range of 0.7 < e_sq < 1.0 for all objects in a given fitsfile (eg. wcs_psf_lsst_000.fits).
I checked if specific file has much bad density than others. The result showed that most the lsst files have about 16-19% bad objects.
There are no any outliers.
```

# Aug 1, 2019
https://nbviewer.jupyter.org/github/bpRsh/2019_shear_analysis_after_dmstack/blob/master/june18_2019/aug1_plot_e1_vs_e2.ipynb

# Aug 9, 2019
https://nbviewer.jupyter.org/github/bpRsh/2019_shear_analysis_after_dmstack/blob/master/june18_2019/aug8_plot_e1_vs_e2.ipynb
