import pandas as pd
from scipy.stats.stats import pearsonr
from plotly.graph_objs import *
from plotly import tools


def validate(data, colNames, colTypes):
    """This function validates the numeric attributes and drops NAN values.
    
    Args:
        data (pandas.DataFrame): The dataframe that columns to be analysed.
        colNames (list): The list of column names to be analysed.
        colTypes (list): The list of column types (numerical or categorical) for each column name in colName. In this case, ['Numeric','Numeric'].
    
    Returns:
        pandas.DataFrame: The modified datframe after validation.
    """
    numericIndices = [i for i, x in enumerate(colTypes) if x == "Numeric"]
    numericCols = [colNames[x] for i,x in enumerate(numericIndices)]
    for col in numericCols:
        data[[col]] = data[[col]].apply(pd.to_numeric, errors = 'coerce')
    data = data.dropna()
    return data


def getScatter(df, colNames):
    """This function creates a graph that plots two datasets with first column as x-axis, and second column as y-axis.
    
    Args:
        df (pandas.DataFrame): The pandas dataframe that contains data columns to be analysed.
        colNames (list): The list of column names to be analysed.
    
    Returns:
        plotly.graph_objs.graph_objs.Figure: A plotly graph for the Scatter plot.
    """
    trace = Scatter(
    x = df[colNames[0]],
    y = df[colNames[1]],
    mode = 'markers',
    marker = dict(
        color = '#119DFF',
        line = dict(width = 1)
        )
    )
    data = [trace]
    layout = Layout(title = 'Scatter plot of the data across ' + colNames[0] + ' and '+ colNames[1],
          hovermode = 'closest',
          xaxis = dict(
          title = colNames[0],
          ticklen = 5),
          yaxis = dict(
          title = colNames[1],
          ticklen = 5))        
    return(Figure(data=data,layout=layout))
 
    
def getBoxPlotComparison(df, colNames):
    """This function creates a box plot of two datasets compared aganist each other.
    
    Args:
        df (pandas.DataFrame): The pandas dataframe that contains data columns to be analysed.
        colNames (list): The list of column names to be analysed.
    
    Returns:
        plotly.graph_objs.graph_objs.Figure: A plotly graph for the box plot.
    """
    trace1 = Box(
        y = df[colNames[0]],
        name = colNames[0],
        marker = dict(
            color = 'rgb(8, 81, 156)',
        ),
        boxmean = True
    )   
    trace2 = Box(
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
    return(fig)


def getCorr(df, colNames):
    """This function creates a table that contains correlation coefficient, p value and a small summary of the two numeric columns.
    
    Args:
        df (pandas.DataFrame): The pandas dataframe that contains data columns to be analysed.
        colNames (list): The list of column names to be analysed.
    
    Returns:
        plotly.graph_objs.graph_objs.Figure: A plotly graph for table.
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
    trace = Table(
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
    fig = Figure(data=data, layout=Layout( dict(title = "Correlation Table for " + str(colNames[0]) +", " + str(colNames[1])) ) )
    return(fig)


def getSkewComparison(df, colNames):
    """This function creates histogram graphs of the two datasets compared aganist each other.
    
    Args:
        df (pandas.DataFrame): The pandas dataframe that contains data columns to be analysed.
        colNames (list): The list of column names to be analysed.
    
    Returns:
        plotly.graph_objs.graph_objs.Figure: A plotly graph for the histogram.
    """
    trace1 = Histogram(
            x = df[colNames[0]], 
            name = colNames[0],   
             marker = dict(color='rgb(0, 0, 100)'))
    trace2 = Histogram(
            x = df[colNames[1]], 
            name = colNames[1],
            marker = dict(color='rgb(8, 81, 156)'))
    fig = tools.make_subplots(rows=1, cols=2)
    fig.append_trace(trace1, 1, 1)
    fig.append_trace(trace2, 1, 2)
    fig['layout'].update(title='Skewness comparison between '+colNames[0]+' and '+colNames[1])
    return(fig)


def getSkewConclusion(df, colNames):
    """This function creates a table for short analysis on the Skewness of the dataset.
    
    Args:
        df (pandas.DataFrame): The pandas dataframe that contains data columns to be analysed.
        colNames (list): The list of column names to be analysed.
    
    Returns:
        plotly.graph_objs.graph_objs.Figure: A plotly graph for the table.
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
    
    trace = Table(
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
    layout = Layout(dict(title = "Skewness conclusion for " + str(colNames[0]) +", " + str(colNames[1])))
    fig = Figure(data=data, layout=layout)
    return(fig)


def getStatsComparison(df, colNames):
    """This function creates a table that lists out basic statistic result on the two datasets, such as mean, median, standard deviation, etc.
    
    Args:
        df (pandas.DataFrame): The pandas dataframe that contains data columns to be analysed.
        colNames (list): The list of column names to be analysed.
    
    Returns:
        plotly.graph_objs.graph_objs.Figure: A plotly graph for the table.
    """
    
    table1 = df[colNames[0]].describe()
    table2 = df[colNames[1]].describe()
    description=['Total count', 'Average value','Standard deviation','Minimun value', 'First Quartile (25%)', 'Median (50%)', 'Third Quartile (75%)','Maximun value']
    trace = Table(
    header = dict(
    values = [['<b>Basic statistic comparison</b>'],
                  ["<b> %s </b>" % (colNames[0])],["<b> %s </b>" % (colNames[1])]],
    line = dict(color = '#506784'),
    fill = dict(color = '#119DFF'),
    align = ['left','center'],
    font = dict(color = 'white', size = 12),
    height = 40
  ),
    cells=dict(values=[description,table1,table2],
               line = dict(color = '#506784'),
                fill = dict(color = ['#25FEFD', 'white']),
                align = ['left', 'center'],
                font = dict(color = '#506784', size = 12),
                height = 30))
    data1 = [trace]  
    layout = Layout(dict(title = "Summary Table for " + str(colNames[0]) +", " + str(colNames[1])))
    fig = Figure(data=data1, layout=layout)
    return (fig)


def TwoNumZeroCat(df, colNames, colTypes):
    """This function calls the statisitcal methods that generate output graphs.
    
    Args:
        df (pandas.DataFrame): The dataframe that columns to be analysed.
        colNames (list): The list of column names to be analysed.
        colTypes (list): The list of column types (numerical or categorical) for each column name in colName. In this case, ['Numeric','Numeric'].
    
    Returns:
        String: A serialized json string of a list of json serialized plotly graphs.
    """
    df = validate(df, colNames, colTypes)
    return ([getStatsComparison(df, colNames), getBoxPlotComparison(df, colNames), getSkewComparison(df, colNames), getSkewConclusion(df, colNames), getScatter(df, colNames), getCorr(df, colNames)])