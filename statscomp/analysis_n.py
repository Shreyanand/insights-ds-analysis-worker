import pandas as pd
import plotly.graph_objs as go
import plotly.figure_factory as ff

    
def oneNumBox(df, colName):
    """This function creates a box plot for the column distribution of colName.
    
    Args:
        df (pandas.DataFrame): The pandas dataframe that contains data columns to be analysed.
        colName (list): The list of column names to be analysed. In this case, the list has one element.
    
    Returns:
        dict: A dict with box plot plotly graph and its label.
    """
    
    boxData = [go.Box(x=df[colName[0]], name=colName[0])]
    layout = go.Layout(title='Box Plot for distribution of ' + str(colName[0]))
    fig = go.Figure(data = boxData, layout = layout)
    return {"label":"Boxplot", "plot":fig}


def oneNumBar(df, colName):
    """This function creates a bar plot for the column colName.
    
    Args:
        df (pandas.DataFrame): The pandas dataframe that contains data columns to be analysed.
        colName (list): The list of column names to be analysed. In this case, the list has one element.
    
    Returns:
        dict: A dict with bar plot plotly graph and its label.
    """
    bins = pd.qcut(x=df[colName[0]], q=15, duplicates='drop')
    ax = bins.value_counts()
    bins = bins.cat.as_ordered()
    bins = bins.cat.categories
    bounds = bins.left 
    bounds = list(bounds)
    bounds.append(bins[len(bounds)-1].right)
    texts = []
    for x,y in zip(bounds[0::],bounds[1::]):
        texts.append("(" + str(x) + ", " + str(y) + "]")    
    barData = [go.Bar(x=texts, 
                     y=ax,
                     marker=dict(
                     color = '#92c5de',
                     opacity=0.8)
                )]  
    layout = go.Layout(
    title="Bar Plot Showing Count of Values for " + str(colName[0]),
    xaxis=dict(
        title= colName[0]
    ),
    yaxis=dict(
        title= "NUMBER OF RECORDS",      
        )
    )
    fig = go.Figure(data=barData, layout=layout)
    return {"label":"Frequency", "plot":fig}


def oneNumDist(df, colName):
    """This function creates a distribution plot for the column colName.
    
    Args:
        df (pandas.DataFrame): The pandas dataframe that contains data columns to be analysed.
        colName (list): The list of column names to be analysed. In this case, the list has one element.
    
    Returns:
        dict: A dict with distribution plot plotly graph and its label.
    """
    
    distData = [df[colName[0]]]
    group_labels = ['colName']
    fig = ff.create_distplot(distData, group_labels, show_hist=False, show_rug = False)
    fig['layout'].update(title='Distribution of ' + str(colName[0]))
    fig['layout'].update(xaxis=dict(title= colName[0]))
    fig['layout'].update(yaxis=dict(title="Probability Density"))
    return {"label":"Distribution", "plot":fig}
