import pandas as pd
import plotly.graph_objs as go
import plotly.figure_factory as ff


def cat_vs_num_recs(data, type_col):
    """This function genetates a bar plot with the column name on x axis and the total counts on y axis.
    
    Args:
        data (pandas.DataFrame): The pandas dataframe that contains records of the top 10 categories.
        type_col (dict):  A dictionary with keys as the data type (Categorical, Numeric, etc) and values as the names of the columns.
            
    Returns:
        dict: A dict with plotly bar graph and its label.
    """
    
    cat_data = 'Categorical' 
    x = data[type_col[cat_data]].tolist()
    y = data['count'].tolist()
    plot_data = [go.Bar(x=x, 
                     y=y,
                     marker=dict(
                        color = '#92c5de',
                        opacity=0.8,
                ))]
    hx=1
    lth = len(x)
    
    layout = go.Layout(
    title="NUMBER OF RECORDS FOR TOP " + str(lth) + " " + type_col[cat_data].upper() + "S",
    xaxis=dict(
        title= type_col[cat_data].upper(),
        tickvals=[0.5 + ((2*k-1)*hx/2) for k in range(0,lth)],
        ticktext=[str(lbl) for lbl in x],
    ),
    yaxis=dict(
        title= "NUMBER OF RECORDS",
        
        )
    )
    fig = go.Figure(data=plot_data, layout=layout)
    return {"label":"Frequency", "plot":fig}


def num_attr_spread(data, type_col):
    """This function gives the spread of the data.
    
    Args:
        data (pandas.DataFrame): The pandas dataframe that contains records of the top 10 categories.
        type_col (dict):  A dictionary with keys as the data type (Categorical, Numeric, etc) and values as the names of the columns.
            
    Returns:
        dict: A dict with spread of data plotly graph and its label.
    """
    
    print("Computing spread of the data...")
    cat_data = 'Categorical' 
    num_data = 'Numeric'
    l = []
    categories = data[type_col[cat_data]].unique()
    colors = ['#b2853b', '#7cb23b', '#39822b', '#45561d', '#3aafa5', '#3a8eae', '#3a67af', '#2b6882', '#164239', '#030906']
    lth = len(categories)
    for i in range(len(categories)):
        
        vals = data.loc[data[type_col[cat_data]] == categories[i]]
        trace0= go.Scattergl(
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
    layout = go.Layout(
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
    fig = go.Figure(data=l, layout=layout)
    return {"label":"Spread", "plot":fig}
  
    
def prob_dist(data, type_col):   
    """This function genetates the probability distribution of the data for the columns.
    
    Args:
        data (pandas.DataFrame): The pandas dataframe that contains records of the top 10 categories.
        type_col (dict):  A dictionary with keys as the data type (Categorical, Numeric, etc) and values as the names of the columns.
            
    Returns:
        dict: A dict with probability distribution plotly graph and its label.
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
    return {"label":"Prob. Distribution", "plot":fig}


def box_plots(data, type_col):
    """This function genetates a box plot depicting the probability distribution of the data for the columns after removing outliers.
    
    Args:
        data (pandas.DataFrame): The pandas dataframe that contains records of the top 10 categories.
        type_col (dict):  A dictionary with keys as the data type (Categorical, Numeric, etc) and values as the names of the columns.
            
    Returns:
        dict: A dict with plotly box graph and its label.
    """
    
    print("Computing probability distribution...")
    
    cat_data = 'Categorical' 
    num_data = 'Numeric'
    categories = data[type_col[cat_data]].unique()
    box_data = []
    group_labels = [str(i) for i in categories]
    colors = ['#b2853b', '#7cb23b', '#39822b', '#45561d', '#3aafa5', '#3a8eae', '#3a67af', '#2b6882', '#164239', '#030906']

    for i in range(len(categories)):
        vals = data.loc[data[type_col[cat_data]] == categories[i]]
        graph_data = go.Box(y= vals[type_col[num_data]],
            name = group_labels[i],
            marker = dict(
                color = colors[i],
            ),
            boxmean = 'sd',
        )
        
        box_data.append(graph_data)
    lth = len(categories)
    layout = go.Layout(
    title = "BOX PLOTS DEPICTING THE DISTRIBUTION OF " + type_col[num_data].upper() + " FOR TOP " + str(lth) + " " + type_col[cat_data].upper() + "S",
    xaxis = dict(
        title= type_col[cat_data].upper(),
        type = "category"
    ),
    yaxis=dict(
        title= type_col[num_data].upper(),
        )
    )
    fig = go.Figure(data=box_data,layout=layout)
    return {"label":"Boxplot", "plot":fig}


def getTop_10(data, colNames, colTypes):
    """This function validates the numeric attributes and drops NAN values.
    
    Args:
        data (pandas.DataFrame): The pandas dataframe that contains data columns to be analysed.
        colNames (list): The list of column names to be analysed.
        colTypes (list): The list of column types (numerical or categorical) for each column name in colName. 
    
    Returns:
        tuple: The tuple of columnName:colType dictionary, dataframe with frequency of top 10 categories, and
        dataframe with values of top 10 categories.
    """
    
    cat_data = 'Categorical' 
    num_data = 'Numeric'
    type_col = {}

    if colTypes[0] == 'Numeric':
        colTypes[0], colTypes[1] = colTypes[1], colTypes[0]
        colNames[0], colNames[1] = colNames[1], colNames[0]
        
    type_col[colTypes[0]] = colNames[0]
    type_col[colTypes[1]] = colNames[1]

    data = data[[type_col[cat_data], type_col[num_data]]]
    temp = data.groupby(type_col[cat_data])[type_col[num_data]].count() 
    df = pd.DataFrame({colNames[0]: temp.index, 'count':temp.values}) #A new dataframe with frequency of categories.
    df = df.sort_values(by='count', ascending=False)[:10]  #taking first 10
    top_10 = data.loc[data[type_col[cat_data]].isin(df[type_col[cat_data]])] #entire data for first 10 categories.
    print("Number of rows for top 10 categories: " + str(top_10.count()[0]))
    return type_col, df, top_10