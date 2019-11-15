import numpy as np
import pandas as pd

import plotly
import plotly.graph_objs as go
import plotly.figure_factory as ff
import plotly.tools as tls
from plotly.offline import plot, iplot, init_notebook_mode
init_notebook_mode(connected=False)

def matrix_of_number_density_from_two_cols(df,xcol,ycol,N):
    """Create grid of number density of two columns
    
    - Find the absolute max from two columns.
    - Create N bins -absMax to +absMax.
    - Return a matrix of N*N shape.
    """
    from itertools import product
    
    # derived variables
    xlabel = xcol
    ylabel = ycol
    xlabel1 = xlabel + '_cat_labels'
    ylabel1 = ylabel + '_cat_labels'
    
    xlabel2 = xlabel + '_cat'
    ylabel2 = ylabel + '_cat'
    colname = 'cat_freq'
    
    # take only xlabel and ylabel columns
    dx = df[[xlabel, ylabel]].copy()
    
    # get absolute maximum from two columns
    tolerance = 0.0000001
    max_abs_xcol_ycol = df[[xcol,ycol]].describe().iloc[[3,-1],:].abs().max().max()
    
    # create 1d array with N+1 values to create N bins
    bins = np.linspace(-max_abs_xcol_ycol-tolerance, max_abs_xcol_ycol+tolerance,N+1)

    # create N bins
    dx[xlabel1] = pd.cut(dx[xlabel], bins, labels=np.arange(N))
    dx[ylabel1] = pd.cut(dx[ylabel], bins, labels=np.arange(N))

    # count number of points in each bin
    dx[colname] = dx.groupby([xlabel1,ylabel1])[xlabel1].transform('count')

    # drop duplicates
    dx1 = dx.drop_duplicates(subset=[xlabel1,ylabel1])[[xlabel1,ylabel1,colname]]

    # use permutation to get the grid of N * N
    perms = list(product(range(N), range(N)))
    x = [i[0] for i in perms]
    y = [i[1] for i in perms]
    dx2 = pd.DataFrame({xlabel1: x, ylabel1: y, colname:0})

    # update dx2 to merge frequency values
    dx2.update(dx2.drop(colname,1).merge(dx1,how='left'))
    dx2 = dx2.astype(int)

    # z values to plot heatmap
    z = dx2[colname].values.reshape(N,N)
    z = z.T

    return z


def transform_scale(z,transform='linear',scale=None):
    """Transform and scale given 1d numpy array.
    
    transform: linear, log, sqrt, sinh, arcsinh
    scale    : minmax, zscale
    
    """
    #==================================
    # linear, log, sqrt, arcsinh, sinh 
    #
    # we need linear tranform option to compare.
    if transform == 'linear':
        z = z

    if transform == 'log':
        z = np.log1p(z)
        
    if transform == 'sqrt':
        z = np.sqrt(z)
        
    if transform == 'sinh':
        z = np.sinh(z)
        
    if transform == 'arcsinh':
        z = np.arcsinh(z)
    
    #===============================
    # scaling minmax and zscale
    if scale== 'minmax':
        z = z / (z.max()-z.min())
    if scale == 'zscale':
        z = (z-z.mean()) / z.std()
        
    return z

def plot_contour(Z,colorscale):

    data = [go.Contour(z=Z, colorscale=colorscale)]
    axis_layout = dict(
        showgrid = True,
        gridcolor='red',
        showticklabels = True
    )

    layout = go.Layout(
        width=650,
        height=600,
        autosize=False,
        xaxis = axis_layout,
        yaxis = axis_layout,
    )

    fig = go.Figure( data=data, layout=layout )

    iplot(fig)
    return None


from ipywidgets import interact

data = matrix_of_number_density_from_two_cols(df,'gsq','gmdsq',10)
data_dict = {'data': data}

transform = ['log','sqrt','arcsinh','sinh','linear']
scale = ['minmax','zscale']
colorscales = ['Blackbody','Bluered','Blues','Earth','Electric','Greens',
'Greys','Hot','Jet','Picnic','Portland','Rainbow','RdBu','Reds',
'Viridis','YlGnBu','YlOrRd']


@interact
def plot_contour_transform_scale(transform=transform,scale=scale,
    colorscale=colorscales, data = data_dict.keys()):
    z = data_dict[data]
    z1 = transform_scale(z,transform=transform,scale=scale)
    plot_contour(z1,colorscale=colorscale)
