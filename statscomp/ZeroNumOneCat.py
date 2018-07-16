import pandas as pd
from scipy import stats
import plotly.graph_objs as go


def getCharts(df, colNames):
    """This function selects between a pie chart and a bar chart and calls their respective function.
    
    Args:
        df (pandas.DataFrame): The pandas dataframe that contains data columns to be analysed.
        colNames (list): The list of column names to be analysed.
    
    Returns:
        plotly.graph_objs.graph_objs.Figure: A plotly graph for either bar or pie chart.
    """
    labels = []
    sizes = []
    
    for i in range(df.shape[0]):
        labels.append(df[colNames[0]][i])
        sizes.append(df['count'][i])

    if len(labels) < 10:
        return getPie(df,colNames)
    else:
        return getBar(df,colNames)
    
    
def getBar(data, colNames):
    """This function creates a bar chart that represents the count of records in the data set that belong to top 10 categories.
    
    Args:
        data (pandas.DataFrame): The pandas dataframe that contains data columns to be analysed.
        colNames (list): The list of column names to be analysed.
    
    Returns:
        plotly.graph_objs.graph_objs.Figure: A plotly graph for the bar chart.
    """
    data = data.values
    data = data[:10]
    plot = [go.Bar(x=str(data[:, 1]),
                y=data[:, 2],
                marker=dict(
                    color='rgb(158,202,225)',
                    line=dict(
                        color='rgb(8,48,107)',
                        width=1.5,
                    )
                ),
                opacity=0.6
    )]
    layout = go.Layout(
        title="Number of Records for the Top " + str(len(data[:,1])) + " " + colNames[0] + "s",
        xaxis=dict(
            title=colNames[0],
            tickvals=[k for k in range(0,len(data[:,1]))],
            ticktext=[str(label) for label in data[:, 1]],        
        ),
        yaxis=dict(
            title="Number of records",
        )
    )
    fig = go.Figure(data=plot, layout=layout)
    return (fig)


def getPie(data, colNames):
    """This function creates a pie chart that represents the count of records in the data set that belong to each categories.
    
    Args:
        data (pandas.DataFrame): The pandas dataframe that contains data columns to be analysed.
        colNames (list): The list of column names to be analysed.
    
    Returns:
        plotly.graph_objs.graph_objs.Figure: A plotly graph for the pie chart.
    """
    data = data.values
    plot = [go.Pie(labels=data[:, 1],
                values=data[:, 2],
                hoverinfo='label+percent',
                opacity=0.6
    )]
    layout = go.Layout(
        title=str(len(data[:,1])) + " " + colNames[0] + " Shown Proportionally"
    )
    fig = go.Figure(data=plot, layout=layout)
    return (fig)


def getStats(temp, colNames):
    """This function creates a summary table for the column colNames.
    
    Args:
        temp (pandas.DataFrame): The pandas dataframe that contains data columns to be analysed.
        colNames (list): The list of column names to be analysed. In this case, the list has only one element.
    
    Returns:
        plotly.graph_objs.graph_objs.Figure: A plotly graph for the summary table.
    """
    df = pd.DataFrame({colNames[0]: temp.index, 'count':temp.values})
    stat=temp.describe()
    max_col_names = df.loc[df['count']==stat[7], colNames[0]].iloc[0]
    min_col_names = df.loc[df['count']==stat[3], colNames[0]].iloc[0]
    skew = 'right' if stats.describe(temp.values)[4] > 0 else 'left'  
    header = ['Total Number of Categories', 'Max Count', 'Min Count', 'Average Count', 'Max Category', 'Min Category', 'Q1', 'Median', 'Q3', 'Skewness']
    data = [stat[0], stat[7], stat[3], round(stat[1],2), max_col_names, min_col_names, stat[4],stat[5], stat[6], skew] 
    tblData = go.Table(
            header=dict(values=header,
                        line = dict(color='#7D7F80'),
                        fill = dict(color='#a1c3d1')),
            cells=dict(values=data,
                       line = dict(color='#7D7F80'),
                       fill = dict(color='#EDFAFF')))
    layout = go.Layout(dict(title = "Summary Table for " + str(colNames[0])))
    data = [tblData]
    fig = go.Figure(data=data, layout=layout)
    return(fig)


def ZeroNumOneCat(df, colNames, colTypes):
    """This function calls the statisitcal methods that generate output graphs.
    
    Args:
        df (pandas.DataFrame): The dataframe that columns to be analysed.
        colNames (list): The list of column names to be analysed.
        colTypes (list): The list of column types (numerical or categorical) for each column name in colName. In this case, ['Categorical']
    
    Returns:
        String: A serialized json string of a list of json serialized plotly graphs.
    """
    if (len(colNames) == 1) and (colTypes[0] == 'Categorical'):
        temp = df.groupby(colNames[0])[colNames[0]].count()
        df = pd.DataFrame({colNames[0]: temp.index, 'count':temp.values})
        df = df.sort_values(by=['count'], ascending=False).reset_index()
        return([getStats(temp, colNames), getCharts(df, colNames)])
    else:
        print("Please input one single categorical variable.")
