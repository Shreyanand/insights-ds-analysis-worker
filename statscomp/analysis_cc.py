import plotly.graph_objs as go
from plotly import tools
import operator


def countBarChart(df, colNames):
    """This function creates a bar chart graph that shows frequency of the entries for each category, and total number of unique entries for each category.

    Args:
        df (pandas.DataFrame): The pandas dataframe that contains data columns to be analysed.
        colNames (list): The list of column names to be analysed.

    Returns:
        dict: A dict with plotly bar graph and its label.
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


def topAccounts(df, colNames):
    """This function creates a table that shows top 10 accounts that appear for two given categories.

    Args:
        df (pandas.DataFrame): The pandas dataframe that contains data columns to be analysed.
        colNames (list): The list of column names to be analysed.

    Returns:
        dict: A dict with plotly bar graph and its label.
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
        y1 = list(dict(df.groupby(colNames[0])[colNames[0]].count()).values())

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
