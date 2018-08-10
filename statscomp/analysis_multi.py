#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 19 13:06:43 2018

@author: shrey
"""

import pandas as pd
import plotly.graph_objs as go
import numpy as np
import scipy.stats as stats

def correlationMatrix (colNames, corr_vals, variableType):
    """This function generates a heatmap of correlation values between features.
    
    Args:
        colNames (list): The list of column names to be analysed.
        corr_vals (list): The list of values for the correlation matrix.
        variableType (String): The type of variable, numeric or categorical.
    
    Returns:
        dict: A dict with heatmap plotly graph and its label.
    """
    
    if variableType == "Numeric":
        z = [-1,1]
        label = "Corr. Matrix N"
    else:
        z = [0,1]
        label = "Corr. Matrix C"
        
    trace = {
      "x": colNames,
      "y": colNames,
      "z": corr_vals,
      "colorscale": [[0.0, 'rgb(165,0,38)'], [0.1111111111111111, 'rgb(215,48,39)'], [0.2222222222222222, 'rgb(244,109,67)'], [0.3333333333333333, 'rgb(253,174,97)'], [0.4444444444444444, 'rgb(254,224,144)'], [0.5555555555555556, 'rgb(224,243,248)'], [0.6666666666666666, 'rgb(171,217,233)'], [0.7777777777777778, 'rgb(116,173,209)'], [0.8888888888888888, 'rgb(69,117,180)'], [1.0, 'rgb(49,54,149)']], 
      "name": "Correlation matrix", 
      "type": "heatmap", 
      "zmax": z[1], 
      "zmin": z[0]
    }
    data = [trace]
    layout = {
      "autosize": False, 
      "bargap": 0.2, 
      "bargroupgap": 0, 
      "barmode": "group", 
      "boxgap": 0.3, 
      "boxgroupgap": 0.3, 
      "boxmode": "overlay", 
      "dragmode": "zoom", 
      "font": {
        "color": "#444", 
        "family": "\"Open sans\", verdana, arial, sans-serif", 
        "size": 12
      }, 
      "height": 540, 
      "hidesources": False, 
      "hovermode": "x", 
      "legend": {
        "bgcolor": "#fff", 
        "bordercolor": "#444", 
        "borderwidth": 10, 
        "font": {
          "color": "#444", 
          "family": "\"Open sans\", verdana, arial, sans-serif", 
          "size": 12
        }, 
        "traceorder": "normal"
      }, 
      "margin": {
        "r": 200, 
        "t": 60, 
        "autoexpand": True, 
        "b": 60, 
        "l": 70, 
        "pad": 2
      }, 
      "paper_bgcolor": "#fff", 
      "plot_bgcolor": "#fff", 
      "separators": ".,", 
      "title": "Correlation matrix", 
      "titlefont": {
          "color": "#444", 
          "family": "\"Open sans\", verdana, arial, sans-serif", 
          "size": 12
      }, 
      "width": 700
    }
    fig = go.Figure(data=data, layout=layout)
    return {"label":label, "plot":fig}
    

def correlationNumerical(df, colNames): return(correlationMatrix (colNames,  df[colNames].corr().values.tolist(), "Numeric"))   
    
    
def numericalDescription(df, colNames):
    """This function creates a table that lists out basic statistic result on the two datasets, such as mean, median, standard deviation, etc.
    
    Args:
        df (pandas.DataFrame): The pandas dataframe that contains data columns to be analysed.
        colNames (list): The list of column names to be analysed.
    
    Returns:
        dict: A dict with summary statistics plotly table and its label.
    """
    
    table = [df[i].describe() for i in colNames]
    description=['Total count', 'Average value','Standard deviation','Minimum value', 'First Quartile (25%)', 'Median (50%)', 'Third Quartile (75%)','Maximum value']
    cell_value = [description] + table
    header_value = [['<b>Basic statistic comparison</b>']] + [["<b> %s </b>" % (i)] for i in colNames]
    trace = go.Table(
    header = dict(
        values = header_value,
        line = dict(color = '#506784'),
        fill = dict(color = '#119DFF'),
        align = ['left','center'],
        font = dict(color = 'white', size = 12),
        height = 40
      ),
        cells = dict(values=cell_value,
                   line = dict(color = '#506784'),
                    fill = dict(color = ['#25FEFD', 'white']),
                    align = ['left', 'center'],
                    font = dict(color = '#506784', size = 12),
                    height = 30)
    )
    data1 = [trace]  
    layout = go.Layout(dict(title = "Summary Table for " + str([i for i in colNames])))
    fig = go.Figure(data=data1, layout=layout)
    return {"label":"Description N", "plot":fig}
        

def categoricalDescription(df, colNames):
    """This function creates a table that shows the analysis of appearnce count of the columns.

    Args:
        df (pandas.DataFrame): The pandas dataframe that contains data columns to be analysed.
        colNames (list): The list of column names to be analysed.
        
    Returns:
        dict: A dict summary statistics plotly table and its label.
    """
    
    description=['Total count', 'Average value','Standard deviation','Minimum value', 'First Quartile (25%)', 'Median (50%)', 'Third Quartile (75%)','Maximum value', 'Maximum Value Category','Minimum Value Category']
    header_value = [['<b>Basic statistic comparison</b>']] + [["<b> %s </b>" % (i)] for i in colNames]
    
    label = ['count']    
    cols = len(colNames)
    cell_value = [description]
    for i in range(cols):
        count = df.groupby(colNames[i])[colNames[i]].count()
        df_count = pd.DataFrame({colNames[i]: count.index, 'count':count.values}) #A new dataframe with frequency of categories.
        table = list(df_count[label].describe()['count'])
        max_col_names = df_count.loc[df_count['count']==table[7],colNames[i]].iloc[0] #Finding maximum count category name.
        min_col_names = df_count.loc[df_count['count']==table[3],colNames[i]].iloc[0]
        table.extend([max_col_names, min_col_names])
        cell_value = cell_value + [table]
    
    trace = go.Table(
    header = dict(
    values = header_value,
    line = dict(color = '#506784'),
    fill = dict(color = '#119DFF'),
    align = ['left','center'],
    font = dict(color = 'white', size = 12),
    height = 40
  ),
    cells=dict(values=cell_value,
               line = dict(color = '#506784'),
                fill = dict(color = ['#25FEFD', 'white']),
                align = ['left', 'center'],
                font = dict(color = '#506784', size = 12),
                height = 30))
    data = [trace]
    layout = go.Layout(dict(title = "Summary Table for " + str([i for i in colNames])))
    fig = go.Figure(data=data, layout=layout)
    return {"label":"Description C", "plot":fig}

#https://stackoverflow.com/questions/46498455/categorical-features-correlation
def cramersV(confusion_matrix):
    """ calculate Cramers V statistic for categorial-categorial association.
        uses correction from Bergsma and Wicher,
        Journal of the Korean Statistical Society 42 (2013): 323-328
        
        Args:
            confusion_matrix (numpy.ndarray): Confusion matrix of features.
    """
    
    chi2 = stats.chi2_contingency(confusion_matrix)[0]
    n = confusion_matrix.sum()
    phi2 = chi2 / n
    r, k = confusion_matrix.shape
    phi2corr = max(0, phi2 - ((k-1)*(r-1))/(n-1))
    rcorr = r - ((r-1)**2)/(n-1)
    kcorr = k - ((k-1)**2)/(n-1)
    return np.sqrt(phi2corr / min((kcorr-1), (rcorr-1)))


def correlationCategorical(df, colNames):
    """This function correlation matrix for categorical variables using cramersV test.

    Args:
        df (pandas.DataFrame): The pandas dataframe that contains data columns to be analysed.
        colNames (list): The list of column names to be analysed.
        
    Returns:
        dict: A dict with heatmap plotly graph and its label.
    """
    
    print("Computing correlation matrix...")
    l = len(colNames)
    cor_matrix = np.empty([l,l])

    for i in range(l):
        cor_matrix[i,i] = 1
        for j in range(i+1,l):
            a = df[colNames[i]]
            b = df[colNames[j]]
            if len(a.unique()) * len(b.unique()) > 3000000000:
                print (" Correlation computation for ",colNames[i]," and ", colNames[j], " is too spacially expensive to handle")
                cor_matrix[i,j] = 0
            else:
                confusion_matrix = pd.crosstab(a, b).values
                cor_matrix[i,j] = cor_matrix[j,i] = cramersV(confusion_matrix)
    return(correlationMatrix (colNames,  cor_matrix.tolist(), "Categorical"))