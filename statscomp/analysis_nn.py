from scipy.stats.stats import pearsonr
import plotly.graph_objs as go
from plotly import tools


def boxPlotComparison(df, colNames):
    """This function creates a box plot of two datasets compared aganist each other.
    
    Args:
        df (pandas.DataFrame): The pandas dataframe that contains data columns to be analysed.
        colNames (list): The list of column names to be analysed.
    
    Returns:
        dict: A dict with box plot plotly graph and its label.
    """
    
    trace1 = go.Box(
        y = df[colNames[0]],
        name = colNames[0],
        marker = dict(
            color = 'rgb(8, 81, 156)',
        ),
        boxmean = True
    )   
    trace2 = go.Box(
        y = df[colNames[1]],
        name = colNames[1],
        marker = dict(
            color = 'rgb(8, 81, 156)',
        ),
        boxmean = True
    )
    fig = tools.make_subplots(rows=1, cols=2)
    fig.append_trace(trace1, 1, 1)
    fig.append_trace(trace2, 1, 2)
    fig['layout'].update(title='Box plot comparison between '+colNames[0]+' and '+colNames[1])
    return {"label":"Comparison", "plot":fig}
    

def skewComparison(df, colNames):
    """This function creates histogram graphs of the two datasets compared aganist each other.
    
    Args:
        df (pandas.DataFrame): The pandas dataframe that contains data columns to be analysed.
        colNames (list): The list of column names to be analysed.
    
    Returns:
        dict: A dict with skew comparison plotly histogram and its label.
    """
    
    trace1 = go.Histogram(
            x = df[colNames[0]], 
            name = colNames[0],   
             marker = dict(color='rgb(0, 0, 100)'))
    trace2 = go.Histogram(
            x = df[colNames[1]], 
            name = colNames[1],
            marker = dict(color='rgb(8, 81, 156)'))
    fig = tools.make_subplots(rows=1, cols=2)
    fig.append_trace(trace1, 1, 1)
    fig.append_trace(trace2, 1, 2)
    fig['layout'].update(title='Skewness comparison between '+colNames[0]+' and '+colNames[1])
    return {"label":"Skewness", "plot":fig}


def skewConclusion(df, colNames):
    """This function creates a table for short analysis on the Skewness of the dataset.
    
    Args:
        df (pandas.DataFrame): The pandas dataframe that contains data columns to be analysed.
        colNames (list): The list of column names to be analysed.
    
    Returns:
        dict: A dict with skew conclusion plotly table and its label.
    """
    
    skew1 = df[colNames[0]].skew()
    skew2 = df[colNames[1]].skew()
    description1 = ''
    description2 = ''
    if skew1 > 1:
        description1 = 'The data has right-skewed distribution, there is a long tail in the positive direction on the number line. The mean is also to the right of the peak.'
    elif skew1 < -1:
        description1 ='The data has left-skewed distribution, there is a long tail in the negative direction on the number line. The mean is also to the left of the peak.'
    else:
        description1 = 'The data has normal distribution.'
        
    if skew2 > 1:
        description2 = 'The data has right-skewed distribution, there is a long tail in the positive direction on the number line. The mean is also to the right of the peak.'
    elif skew2 < -1:
        description2 ='The data has left-skewed distribution, there is a long tail in the negative direction on the number line. The mean is also to the left of the peak.'
    else:
        description2 = 'The data has normal distribution.'
    
    trace = go.Table(
        header = dict(
            values = [['<b>Conclustion</b>']],
            line = dict(color = '#506784'),
            fill = dict(color = '#119DFF'),
            align = ['left','center'],
            font = dict(color = 'white', size = 12),
            height = 40
        ),
        cells=dict(
            values=[["<b> %s: </b>" % (colNames[0])+description1, "<b> %s: </b>" % (colNames[1])+description2]],
            line = dict(color = '#506784'),
            fill = dict(color = ['#25FEFD', 'white']),
            align = ['left', 'center'],
            font = dict(color = '#506784', size = 12),
            height = 30)
    )
    data = [trace]    
    layout = go.Layout(dict(title = "Skewness conclusion for " + str(colNames[0]) +", " + str(colNames[1])))
    fig = go.Figure(data=data, layout=layout)
    return {"label":"Skew Conclusion", "plot":fig}


def scatter(df, colNames):
    """This function creates a graph that plots two datasets with first column as x-axis, and second column as y-axis.
    
    Args:
        df (pandas.DataFrame): The pandas dataframe that contains data columns to be analysed.
        colNames (list): The list of column names to be analysed.
    
    Returns:
        dict: A dict with scatter plotly graph and its label.
    """
    
    trace = go.Scatter(
    x = df[colNames[0]],
    y = df[colNames[1]],
    mode = 'markers',
    marker = dict(
        color = '#119DFF',
        line = dict(width = 1)
        )
    )
    data = [trace]
    layout = go.Layout(title = 'Scatter plot of the data across ' + colNames[0] + ' and '+ colNames[1],
          hovermode = 'closest',
          xaxis = dict(
          title = colNames[0],
          ticklen = 5),
          yaxis = dict(
          title = colNames[1],
          ticklen = 5))        
    fig = go.Figure(data=data,layout=layout)
    return {"label":"Scatter", "plot":fig}

def corr(df, colNames):
    """This function creates a table that contains correlation coefficient, p value and a small summary of the two numeric columns.
    
    Args:
        df (pandas.DataFrame): The pandas dataframe that contains data columns to be analysed.
        colNames (list): The list of column names to be analysed.
    
    Returns:
        dict: A dict with correlation plotly table and its label.
    """
    
    corr = pearsonr([int(i) for i in df[colNames[0]].tolist()],[int(i) for i in df[colNames[1]].tolist()])
    strength = '';
    sign = '';
    sig=' '
    conclusion = '';
    r=abs(corr[0])
    if r >0.1 and r < 0.3:
        strength = 'small correlation'
    elif r >0.3 and r < 0.5:
        strength = 'medium/moderate correation'
    elif r >0.5:
        strength = 'large/strong correlation'
    else:
        strength = 'no correlation'
    if corr[0] > 0:
        sign = 'positive'
    else:
        sign = 'negative'

    if corr[1] < 0.05:
        sig = 'statistically significant'
    else:
        sig = 'statistically insignificant'

    if strength == 'no correlation':
        conclusion = 'Two datasets have no correlation'
    else:
        conclusion='Two datasets have '+ sign + ' '+ strength +' and this result is ' + sig +'.'
    table = {'1. The correlation coefficient is': corr[0], '2. P value is': corr[1], '3. Conclusion': conclusion}
    trace = go.Table(
        header = dict(
            values = [['<b>Simple Analysis on Correlation</b>'],
                      ['<b>Result</b>']],
            line = dict(color = '#506784'),
            fill = dict(color = '#119DFF'),
            align = ['left','center'],
            font = dict(color = 'white', size = 12),
            height = 40
        ),
        cells=dict(
            values=[list(table.keys()), list(table.values())],
            line = dict(color = '#506784'),
            fill = dict(color = ['#25FEFD', 'white']),
            align = ['left', 'center'],
            font = dict(color = '#506784', size = 12),
            height = 30)
    )
    data = [trace]
    fig = go.Figure(data=data, layout=go.Layout( dict(title = "Correlation Table for " + str(colNames[0]) +", " + str(colNames[1])) ) )
    return {"label":"Correlation", "plot":fig}