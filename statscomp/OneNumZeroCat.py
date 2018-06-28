import pandas as pd
import numpy as np
import scipy.stats as stats
from plotly.graph_objs import *
import plotly.figure_factory as ff


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
        data[col] = pd.to_numeric(data[col],errors='coerce')
        data = data[data[col].notnull()]
    return data


def oneNumTable(df, colName): 
    """This function creates a summary table for the column colName.
    
    Args:
        df (pandas.DataFrame): The pandas dataframe that contains data columns to be analysed.
        colName (list): The list of column names to be analysed. In this case, the list has one element.
    
    Returns:
        plotly.graph_objs.graph_objs.Figure: A plotly graph for summary table
    """
    
    lstColVal = list(df.describe(percentiles = [0.25, 0.50, 0.75])[colName[0]]) 
    if (stats.skew(lstColVal)) > 0.0:

        tblData = Table(

            header=dict(values=['Min','Max', 'Count', 'Average', 'Stdev', '1st Quartile', '2nd Quartile', '3rd Quartile', 'Skewness'],
                        line = dict(color='#7D7F80'),
                        fill = dict(color='#a1c3d1'),
                        align = ['left'] * 5),
            cells=dict(values=[[int(lstColVal[3])], 
                               [int(lstColVal[7])], 
                               [int(lstColVal[0])], 
                               [int(lstColVal[1])],
                               [int(lstColVal[2])], 
                               [int(lstColVal[4])], 
                               [int(lstColVal[5])], 
                               [int(lstColVal[6])], 
                               ["Right"]
        ],
                       line = dict(color='#7D7F80'),
                       fill = dict(color='#EDFAFF'),
                       align = ['left'] * 5))
        
    elif (stats.skew(lstColVal)) < 0:
        tblData = Table(

            header=dict(values=['Min','Max', 'Count', 'Average', 'Stdev', '1st Quartile', '2nd Quartile', '3rd Quartile', 'Skewness'],
                        line = dict(color='#7D7F80'),
                        fill = dict(color='#a1c3d1'),
                        align = ['left'] * 5),
            cells=dict(values=[[int(lstColVal[3])], 
                               [int(lstColVal[7])], 
                               [int(lstColVal[0])], 
                               [int(lstColVal[1])],
                               [int(lstColVal[2])], 
                               [int(lstColVal[4])], 
                               [int(lstColVal[5])], 
                               [int(lstColVal[6])], 
                               ["Left"]
        ],
                       line = dict(color='#7D7F80'),
                       fill = dict(color='#EDFAFF'),
                       align = ['left'] * 5))
    else:
        tblData = Table(

            header=dict(values=['Min','Max', 'Count', 'Average', 'Stdev', '1st Quartile', '2nd Quartile', '3rd Quartile', 'Skewness'],
                        line = dict(color='#7D7F80'),
                        fill = dict(color='#a1c3d1'),
                        align = ['left'] * 5),
            cells=dict(values=[[int(lstColVal[3])], 
                               [int(lstColVal[7])], 
                               [int(lstColVal[0])], 
                               [int(lstColVal[1])],
                               [int(lstColVal[2])], 
                               [int(lstColVal[4])], 
                               [int(lstColVal[5])], 
                               [int(lstColVal[6])], 
                               ["No Skew"]
        ],
                       line = dict(color='#7D7F80'),
                       fill = dict(color='#EDFAFF'),
                       align = ['left'] * 5))
    
    layout = Layout(dict(title = "Summary Table for " + str(colName[0])))
    data = [tblData]
    layout = Layout()
    fig = Figure(data=data, layout=layout)
    return(fig)

    
def oneNumBox(df, colName):
    """This function creates a box plot for the column distribution of colName.
    
    Args:
        df (pandas.DataFrame): The pandas dataframe that contains data columns to be analysed.
        colName (list): The list of column names to be analysed. In this case, the list has one element.
    
    Returns:
        plotly.graph_objs.graph_objs.Figure: A plotly graph for the box plot.
    """
    
    boxData = [Box(x=df[colName[0]], name=colName)]
    layout = Layout(title='Box Plot for distribution of ' + str(colName[0]))
    fig = Figure(data = boxData, layout = layout)
    return (fig)


def oneNumBar(df, colName):
    """This function creates a bar plot for the column colName.
    
    Args:
        df (pandas.DataFrame): The pandas dataframe that contains data columns to be analysed.
        colName (list): The list of column names to be analysed. In this case, the list has one element.
    
    Returns:
        plotly.graph_objs.graph_objs.Figure: A plotly graph for the bar plot.
    """
    try:
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
        barData = [Bar(x=texts, 
                         y=ax,
                         marker=dict(
                         color = '#92c5de',
                         opacity=0.8)
                    )]  
        layout = Layout(
        title="Bar Plot Showing Count of Values for " + str(colName[0]),
        xaxis=dict(
            title= colName
        ),
        yaxis=dict(
            title= "NUMBER OF RECORDS",      
            )
        )
        fig = Figure(data=barData, layout=layout)
        return (fig)
    except IndexError as e:
        print("Oops! Could not generate the Bar Plot due to a '%s' error! Sorry!"%(str(e)))


def oneNumDist(df, colName):
    """This function creates a distribution plot for the column colName.
    
    Args:
        df (pandas.DataFrame): The pandas dataframe that contains data columns to be analysed.
        colName (list): The list of column names to be analysed. In this case, the list has one element.
    
    Returns:
        plotly.graph_objs.graph_objs.Figure: A plotly graph for the distribution plot.
    """
    try:
        distData = [df[colName[0]]]
        group_labels = ['colName']
        fig = ff.create_distplot(distData, group_labels, show_hist=False, show_rug = False)
        fig['layout'].update(title='Distribution of ' + str(colName[0]))
        fig['layout'].update(xaxis=dict(title= colName[0]))
        fig['layout'].update(yaxis=dict(title="Probability Density"))
        return (fig)
    except np.linalg.LinAlgError as err:
            print("Oops! Cannot plot the Probability Distribution Plot due to a '%s' error! Sorry!"%(str(err)))
            
            
def OneNumZeroCat(df, colNames, colTypes):
    """This function calls the statisitcal methods that generate output graphs.
    
    Args:
        df (pandas.DataFrame): The dataframe that columns to be analysed.
        colNames (list): The list of column names to be analysed.
        colTypes (list): The list of column types (numerical or categorical) for each column name in colName. In this case, ['Numeric'].
    
    Returns:
        String: A serialized json string of a list of json serialized plotly graphs.
    """
    
    df = validate(df,colNames, colTypes)  
    return ([oneNumTable(df, colNames), oneNumBox(df, colNames), oneNumBar(df, colNames), oneNumDist(df, colNames)])