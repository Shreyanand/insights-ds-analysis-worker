import pandas as pd
import plotly.graph_objs as go
from plotly import tools
import operator


def getCountBarChart(df, colNames):
    """This function creates a bar chart graph that shows frequency of the entries for each category, and total number of unique entries for each category.

    Args:
        df (pandas.DataFrame): The pandas dataframe that contains data columns to be analysed.
        colNames (list): The list of column names to be analysed.

    Returns:
        plotly.graph_objs.graph_objs.Figure: A plotly graph for the bar chart.
    """
    trace1 = go.Bar(
        x = [colNames[0],colNames[1]],
        y = [df[colNames[0]].count(), df[colNames[1]].count()],
        name = 'Total counts'
    )
    trace2 = go.Bar(
        x = [colNames[0],colNames[1]],
        y = [df[colNames[0]].nunique(), df[colNames[1]].nunique()],
        name = 'Unique counts'

    )
    data = [trace1, trace2]
    layout = go.Layout(
        barmode = 'group',
        title = 'Count analysis'
    )
    fig = go.Figure(data = data, layout = layout)
    return {"label":"Unique vs Total", "plot":fig}

def getTopAccounts(df, colNames):
    """This function creates a table that shows top 10 accounts that appear for two given categories.

    Args:
        df (pandas.DataFrame): The pandas dataframe that contains data columns to be analysed.
        colNames (list): The list of column names to be analysed.

    Returns:
        plotly.graph_objs.graph_objs.Figure: A plotly graph for the bar chart.
    """
    x1 = []
    y1 = []
    x2 = []
    y2 = []

    if df[colNames[0]].nunique() > 10:
        count = dict(df.groupby(colNames[0])[colNames[0]].count())
        sorted_count = sorted(count.items(), key=operator.itemgetter(1))
        sorted_count.reverse()
        for x in range(10):
            x1.append(sorted_count[x][0])
            y1.append(sorted_count[x][1])
    else:
        x1 = list(dict(df.groupby(colNames[0])[colNames[0]].count()).keys())
        y1 = list(dict(df.groupby(colNames[0])[colNames[0]].count()).keys())

    trace1 = go.Bar(
        x = x1,
        y = y1,
        name = colNames[0]
    )

    if df[colNames[1]].nunique() > 10:
        count = dict(df.groupby(colNames[1])[colNames[1]].count())
        sorted_count = sorted(count.items(), key=operator.itemgetter(1))
        sorted_count.reverse()
        for x in range(10):
            x2.append(sorted_count[x][0])
            y2.append(sorted_count[x][1])
    else:
        x2 = list(dict(df.groupby(colNames[1])[colNames[1]].count()).keys())
        y2 = list(dict(df.groupby(colNames[1])[colNames[1]].count()).values())

    trace2 = go.Bar(
        x = x2,
        y = y2,
        name = colNames[1]
    )
    fig = tools.make_subplots(rows=2, cols=1)
    fig.append_trace(trace1, 1, 1)
    fig.append_trace(trace2, 2, 1)
    fig['layout'].update(height=600, width=600, title='Top accounts for '+colNames[0]+' and '+colNames[1])
    return {"label":"Top Frequency", "plot":fig}


def getAppearanceAanalysis(df, colNames):
    """This function creates a table that shows the analysis of appearnce count of the columns.

    Args:
        df (pandas.DataFrame): The pandas dataframe that contains data columns to be analysed.
        colNames (list): The list of column names to be analysed.

    Returns:
        plotly.graph_objs.graph_objs.Figure: A plotly graph for the table.
    """

    label = ['count']
    count1 = list(df.groupby(colNames[0])[colNames[0]].count())
    df1 = pd.DataFrame(count1, columns = label)
    table1 = list(df1[label].describe()['count'])
    count2 = list(df.groupby(colNames[1])[colNames[1]].count())
    df2 = pd.DataFrame(count2, columns = label)
    table2 = list(df2[label].describe()['count'])
    description=['Total count', 'Average value','Standard deviation','Minimum value', 'First Quartile (25%)', 'Median (50%)', 'Third Quartile (75%)','Maximum value']
    trace = go.Table(
    header = dict(
    values = [['<b>Basic statistic analysis on </b>'],
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
    data = [trace]
    layout = go.Layout(dict(title = "Appearance Count Table for " + str(colNames[0]) +", " + str(colNames[1])))
    fig = go.Figure(data=data, layout=layout)
    return {"label":"Description", "plot":fig}


def ZeroNumTwoCat(data, colNames, colTypes):
    """This function calls the statisitcal methods that generate output graphs.

    Args:
        df (pandas.DataFrame): The dataframe that columns to be analysed.
        colNames (list): The list of column names to be analysed.
        colTypes (list): The list of column types (numerical or categorical) for each column name in colName. In this case, ['Categorical','Categorical'].

    Returns:
        String: A serialized json string of a list of json serialized plotly graphs.
    """
    return([getCountBarChart(data, colNames), getTopAccounts(data, colNames), getAppearanceAanalysis(data, colNames)])
    