import pandas as pd
import numpy as np
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


def cat_vs_num_recs(data, type_col):
    """This function genetates a bar plot with the column name on x axis and the total counts on y axis.
    
    Args:
        data (pandas.DataFrame): The pandas dataframe that contains records of the top 10 categories.
        type_col (dict):  A dictionary with keys as the data type (Categorical, Numeric, etc) and values as the names of the columns.
            
    Returns:
        String: A serialized json string of plotly graphs.
    """
    
    cat_data = 'Categorical' 
    data = data.values
    wid = np.ones(len(data[:,1]))
    plot_data = [Bar(x=str(data[:,1]), 
                     y=data[:,0],
                     width=wid*0.3,
                     marker=dict(
                        color = '#92c5de',
                        opacity=0.8,
                ))]
    hx=1
    lth = len(data[:,1])
    layout = Layout(
    title="NUMBER OF RECORDS FOR TOP " + str(lth) + " " + type_col[cat_data].upper() + "S",
    xaxis=dict(
        title= type_col[cat_data].upper(),
        tickvals=[0.5 + ((2*k-1)*hx/2) for k in range(0,lth)],
        ticktext=[str(lbl) for lbl in data[:,1]],
    ),
    yaxis=dict(
        title= "NUMBER OF RECORDS",     
        )
    )  
    fig = Figure(data=plot_data, layout=layout)
    return (fig)


def num_attr_spread(data, type_col):
    """This function gives the spread of the data.
    
    Args:
        data (pandas.DataFrame): The pandas dataframe that contains records of the top 10 categories.
        type_col (dict):  A dictionary with keys as the data type (Categorical, Numeric, etc) and values as the names of the columns.
            
    Returns:
        String: A serialized json string of plotly graphs.
    """
    
    cat_data = 'Categorical' 
    num_data = 'Numeric'
    l = []
    categories = data[type_col[cat_data]].unique()
    colors = ['#b2853b', '#7cb23b', '#39822b', '#45561d', '#3aafa5', '#3a8eae', '#3a67af', '#2b6882', '#164239', '#030906']
    lth = len(categories)
    for i in range(len(categories)):
        
        vals = data.loc[data[type_col[cat_data]] == categories[i]]
        trace0= Scattergl(
            x= vals[type_col[num_data]],
            y= [str(x) for x in vals[type_col[cat_data]]],
            mode= 'markers',
            marker= dict(size= 14,
                         symbol="line-ns-open",
                        line= dict(width=1),
                        color= colors[i],
                        opacity= 0.5
                       ),
        ) 
        l.append(trace0);
    lth = len(categories)
    layout = Layout(
    showlegend=False,
    title=type_col[num_data].upper() + " VS " + type_col[cat_data].upper() + " FOR TOP " + str(lth) + " " + type_col[cat_data].upper() + "S",
    xaxis=dict(
        title= type_col[num_data].upper(),
    ),
    yaxis=dict(
        title= type_col[cat_data].upper(),
        type= "category"      
        )
    )
    fig = Figure(data=l, layout=layout)
    return(fig)
  
    
def prob_dist(data, type_col):   
    """This function genetates the probability distribution of the data for the columns.
    
    Args:
        data (pandas.DataFrame): The pandas dataframe that contains records of the top 10 categories.
        type_col (dict):  A dictionary with keys as the data type (Categorical, Numeric, etc) and values as the names of the columns.
            
    Returns:
        String: A serialized json string of plotly graphs.
    """
    
    cat_data = 'Categorical' 
    num_data = 'Numeric'
    categories = data[type_col[cat_data]].unique()
    hist_data = []
    group_labels = []
    for category in categories:
        vals = data.loc[data[type_col[cat_data]] == category]
        hist_data.append(vals[type_col[num_data]])      
    group_labels = categories  
    colors = ['#b2853b', '#7cb23b', '#39822b', '#45561d', '#3aafa5', '#3a8eae', '#3a67af', '#2b6882', '#164239', '#030906']
    fig = ff.create_distplot(hist_data, group_labels, show_hist=False, show_rug = False, histnorm='probability density', colors=colors)
    lth = len(categories)
    fig['layout'].update(title='PROBABILITY DENSITY OF ' + type_col[num_data].upper() + " FOR TOP " + str(lth) + " " + type_col[cat_data].upper() + "S")
    fig['layout'].update(xaxis=dict(title=type_col[num_data].upper()))
    fig['layout'].update(yaxis=dict(title="PROBABILITY DENSITY"))
    return (fig)


def box_plots(data, type_col):
    """This function genetates a box plot depicting the probability distribution of the data for the columns after removing outliers.
    
    Args:
        data (pandas.DataFrame): The pandas dataframe that contains records of the top 10 categories.
        type_col (dict):  A dictionary with keys as the data type (Categorical, Numeric, etc) and values as the names of the columns.
            
    Returns:
        String: A serialized json string of plotly graphs.
    """
    
    cat_data = 'Categorical' 
    num_data = 'Numeric'
    categories = data[type_col[cat_data]].unique()
    box_data = []
    group_labels = [str(i) for i in categories]
    colors = ['#b2853b', '#7cb23b', '#39822b', '#45561d', '#3aafa5', '#3a8eae', '#3a67af', '#2b6882', '#164239', '#030906']

    for i in range(len(categories)):
        vals = data.loc[data[type_col[cat_data]] == categories[i]]
        graph_data = Box(y= vals[type_col[num_data]],
            name = group_labels[i],
            marker = dict(
                color = colors[i],
            ),
            boxmean = 'sd',
        )
        
        box_data.append(graph_data)
    lth = len(categories)
    layout = Layout(
    title = "BOX PLOTS DEPICTING THE DISTRIBUTION OF " + type_col[num_data].upper() + " FOR TOP " + str(lth) + " " + type_col[cat_data].upper() + "S",
    xaxis = dict(
        title= type_col[cat_data].upper(),
        type = "category"
    ),
    yaxis=dict(
        title= type_col[num_data].upper(),
        )
    )
    fig = Figure(data=box_data,layout=layout)
    return (fig)


def OneNumOneCat(data, colNames, colTypes):
    """This function calls the statisitcal methods that generate output graphs.
    
    Args:
        df (pandas.DataFrame): The pandas dataframe that contains data columns to be analysed.
        colNames (list): The list of column names to be analysed.
        colTypes (list): The list of column types (numerical or categorical) for each column name in colName. In this case, ['Categorical','Numeric'].
    
    Returns:
        String: A serialized json string of a list of json serialized plotly graphs.
    """
    data = validate(data, colNames, colTypes)
    cat_data = 'Categorical' 
    num_data = 'Numeric'
    
    if len(colTypes)!=2 or len(colNames)!=2:
        print("Function accepts only 2 column names and 2 column types.")
        return
    type_col = {}
    try:
        if colTypes[0] == 'Numeric':
            colTypes[0], colTypes[1] = colTypes[1], colTypes[0]
            colNames[0], colNames[1] = colNames[1], colNames[0]
            
        type_col[colTypes[0]] = colNames[0]
        type_col[colTypes[1]] = colNames[1]
 
        if(len(type_col) != 2):
            print("Function accepts one numerical and one categorical column. Please check the types of columns passed!")
            return
    
        req_data = data[[type_col[cat_data], type_col[num_data]]]
        temp = req_data.groupby(type_col[cat_data])[type_col[num_data]].count()
        df = pd.DataFrame({colNames[0]: temp.index, 'count':temp.values})
        df = df.sort_values(by='count', ascending=False)[:10]  
        cat_vals = df[type_col[cat_data]]
        top_10 = req_data.loc[req_data[type_col[cat_data]].isin(cat_vals)]
        
#        g1 = json.dumps(cat_vs_num_recs(df, type_col), cls=utils.PlotlyJSONEncoder)
#        
#        g2 = json.dumps(num_attr_spread(top_10, type_col), cls=utils.PlotlyJSONEncoder)
#        
#        g3 = json.dumps(prob_dist(top_10,type_col), cls=utils.PlotlyJSONEncoder)
#        
#        g4 = json.dumps(box_plots(top_10,type_col), cls=utils.PlotlyJSONEncoder)
#        
#        g =  {'cat_vs_num_recs':g1, 'num_attr_spread':g2, 'prob_dist':g3, 'box_plots':g4}
#        body = json.dumps(g)
        return ([cat_vs_num_recs(df, type_col), num_attr_spread(top_10, type_col), prob_dist(top_10,type_col), box_plots(top_10,type_col)])
           
    except KeyError as e:
        print("Please check the column name passed - Key Error: %s"%str(e))