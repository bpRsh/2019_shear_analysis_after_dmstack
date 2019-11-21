
|  Notebook | Rendered   | Description  |  Author |
|---|---|---|---|
| a01_plot_gsq_vs_gmdsq.ipynb  | [rendered](https://nbviewer.jupyter.org/github/bpRsh/2019_shear_analysis_after_dmstack/blob/master/Nov_2019/Nov21/a01_plot_gsq_vs_gmdsq.ipynb)  |   | [Bhishan Poudel](https://bhishanpdl.github.io/)  |


# Removed strong lens objects
```python
#define OMEGA_M 0.315       //matter density of the universe today
#define OMEGA_D 0.685       //dark energy density of the universe
#define H0      67.80       //Planck value for Hubble constant for present day [km/(Mps*s)]

Choose g = 0.5 at 138 gives 154 pixels.

# exclude strong lens objects <=154 distance
# The shape of lsst.fits file is 3998,3998 and center is 1699,1699.
df['x_center'] = 1699
df['y_center'] = 1699
df['distance'] = ( (df['x[0]'] - df['x_center'])**2 + (df['x[1]'] - df['y_center'])**2 )**0.5
df = df[df.distance > 154]
```
