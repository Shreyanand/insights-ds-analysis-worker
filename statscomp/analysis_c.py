import pandas as pd
import plotly.graph_objs as go


def charts(df, colNames):
    """This function selects between a pie chart and a bar chart and calls their respective function.
    
    Args:
        df (pandas.DataFrame): The pandas dataframe that contains data columns to be analysed.
        colNames (list): The list of column names to be analysed.
    
    Returns:
        dict: A dict with plotly graph and its label.
    """
    
    temp = df.groupby(colNames[0])[colNames[0]].count()
    df = pd.DataFrame({colNames[0]: temp.index, 'count':temp.values}) #A new dataframe with frequency of categories.
    df = df.sort_values(by=['count'], ascending=False).reset_index()
    
    labels = []
    sizes = []
    
    for i in range(df.shape[0]):
        labels.append(df[colNames[0]][i])
        sizes.append(df['count'][i])

    if len(labels) < 10:
        return pie(df,colNames)
    else:
        return bar(df,colNames)
    
    
def bar(data, colNames):
    """This function creates a bar chart that represents the count of records in the data set that belong to top 10 categories.
    
    Args:
        data (pandas.DataFrame): The pandas dataframe that contains data columns to be analysed.
        colNames (list): The list of column names to be analysed.
    
    Returns:
        dict: A dict with plotly bar graph and its label.
    """
    
    data = data.values
    data = data[:10]
    plot = [go.Bar(x=data[:, 1],
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
    return {"label":"Top Frequency", "plot":fig}


def pie(data, colNames):
    """This function creates a pie chart that represents the count of records in the data set that belong to each categories.
    
    Args:
        data (pandas.DataFrame): The pandas dataframe that contains data columns to be analysed.
        colNames (list): The list of column names to be analysed.
    
    Returns:
        dict: A dict with plotly pie chart and its label.
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
    return {"label":"Top Frequency", "plot":fig}
