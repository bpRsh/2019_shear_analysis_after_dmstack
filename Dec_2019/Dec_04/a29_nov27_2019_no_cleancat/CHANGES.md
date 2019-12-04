# Change Nov 27
```
# Usual workflow
dmstack: l.csv, l9.csv, m.csv, m9.csv
remove nans: l.txt, l9.txt, m.txt, m9.txt  # these are tsv files but I named txt
imcat combine 4 txt files: final_text.txt  (combined 100*4 files to single catalog)
```
Changes made:
Added clean cat commands in imcat script.
```bash
File: a01_combine_four_txts_to_lc_catalog_new

Old:
lc -C -n fN -n id -N '1 2 x' -N '1 2 errx' -N '1 2 g' -n ellip -n flux -n radius < "${LT}".txt > "${LC}".cat


New:
lc -C -n fN -n id -N '1 2 x' -N '1 2 errx' -N '1 2 g' -n ellip -n flux -n radius < "${LT}".txt  | lc +all 'mag = %flux log10 -2.5 *' | cleancat 20 | lc +all -r 'mag' > "${LC}".cat
```
