|  Notebook | Rendered   | Description  |  Author |
|---|---|---|---|
| a01_dmstack_noise_comparison.ipynb  | [ipynb](https://github.com/bpRsh/shear_analysis_after_dmstack/blob/master/Fall_2020/2020_08_24/a01_dmstack_noise_comparison.ipynb), [rendered](https://nbviewer.jupyter.org/github/bpRsh/shear_analysis_after_dmstack/blob/master/Fall_2020/2020_08_24/a01_dmstack_noise_comparison.ipynb)  |   | [Bhishan Poudel](https://bhishanpdl.github.io/)  |
| b01_ngals10k_z1.5_noise50.ipynb  | [ipynb](https://github.com/bpRsh/shear_analysis_after_dmstack/blob/master/Fall_2020/2020_08_24/b01_ngals10k_z1.5_noise50.ipynb), [rendered](https://nbviewer.jupyter.org/github/bpRsh/shear_analysis_after_dmstack/blob/master/Fall_2020/2020_08_24/b01_ngals10k_z1.5_noise50.ipynb)  |   | [Bhishan Poudel](https://bhishanpdl.github.io/)  |


# Object Detection Comparison among ngals-10k-20k-50k and dmstackNoise-50-100
```
"""
Note: total_objs = ngals * 20 (for 20 files)
Note: the input 20 files for ngals5k are different from 10k and 20k
      but files are same for 10k and 20k


data/final_text_cleancat15_ngals5k_z1.5_noise100_000_019.txt 2507
data/final_text_cleancat15_ngals5k_z1.5_noise50_000_019.txt 3651

data/final_text_cleancat15_ngals10k_z1.5_noise100_100_119.txt 5418
data/final_text_cleancat15_ngals10k_z1.5_noise50_100_119.txt 8143
data/final_text_cleancat15_ngals20k_z1.5_noise100_100_119.txt 7473
data/final_text_cleancat15_ngals20k_z1.5_noise50_100_119.txt 10721


cleancat  ngals z    dmstack_noise  objects_detected  total_objs percent
------------------------------------------------------------------------
15        5k    1.5  50             3651              100k       3.65%
15        5k    1.5  100            2507              100k       2.5%
------------------------------------------------------------------------

15        10k   1.5  50             8143              200k       4.07%
15        10k   1.5  100            5418              200k       2.7%
15        20k   1.5  50             10721             400k       2.68%
15        20k   1.5  100            7473              400k       1.86%


Best so far: noise 50 ngals10k  with 4% object detection.
             There are 200k objects in 20 files, but dmstack detected
             only 8k files (4%).
""";

```

| cleancat | ngals | z | dmstack_noise | objects_detected | total_objs | percent |
| :---|:---|:---|:---|:---|:---|:---|
| 15 | 5k | 1.5 | 50 | 3651 | 100k | 3.65% |
| 15 | 5k | 1.5 | 100 | 2507 | 100k | 2.5% |
| 15 | 10k | 1.5 | 50 | 8143 | 200k | 4.07% |
| 15 | 10k | 1.5 | 100 | 5418 | 200k | 2.7% |
| 15 | 20k | 1.5 | 50 | 10721 | 400k | 2.68% |
| 15 | 20k | 1.5 | 100 | 7473 | 400k | 1.86% |


NOTES:  
For these observations I have used 20 files. For 10k num galaxies they have 200k objects and for 20k num galaxies,
they have 100k objects.

From jedisim simulations I have these number of total simulations:
```
ngals10k ==> 162 files
ngals20k ==> 300 files
```
