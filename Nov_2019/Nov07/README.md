**Nov 8, 2019 Friday**  

# Highest and Lowest bad objects density

There are 90 flags and for all cased I have used the filter calib psf candidate is 
False. Using this I get 17.6574% objects in the range 0.5 < gmsq < 1.1.

For most of the flags I see this same number, but for some specific flags I got
some max and in object density.


```bash
Flag Number     Bad%               Flag Names
---------------------------------------------------------------------------------
26, 29       = 17.52% (minimum)   base_SdssShape_flag, base_SdssShape_flag_shift
5            = 19.63% (2nd min)   deblend_deblendedAsPsf
most of them = 17.65%
56           = 17.66%
67,72        = 17.67%
63,66        = 17.68%
0            = 20.28% (2nd max)    calib_detected
85,86        = 20.48% (max)        base_Variance_flag,base_Variance_flag_emptyFootprint
```

# Images
**Flag 0 : calib_detected**
![](results/flags/flag_0.png)

**Flag 1 : calib_psfCandidate (I have used this for all cases)**
![](results/flags/flag_1.png)

**Flag 2 : calib_psfUsed**
![](results/flags/flag_2.png)

**Flag 3 : calib_psfReserved**
![](results/flags/flag_3.png)

**Flag 4 : flags_negative**
![](results/flags/flag_4.png)

**Flag 5 : deblend_deblendedAsPsf**
![](results/flags/flag_5.png)




**Flag 26 : base_SdssShape_flag**
![](results/flags/flag_26.png)

**Flag 29 : base_SdssShape_flag_shift**
![](results/flags/flag_29.png)



**Flag 85 : base_Variance_flag**
![](results/flags/flag_85.png)

**Flag 86 : base_Variance_flag_emptyFootprint**
![](results/flags/flag_86.png)
