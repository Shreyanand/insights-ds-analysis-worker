import os
import sys
import traceback
import s3fs
import statscomp.analysis_nc as nc
import statscomp.analysis_n as on
import statscomp.analysis_nn as nn
import statscomp.analysis_c as oc
import statscomp.analysis_cc as cc
import statscomp.analysis_multi as mf
import statscomp.utilities as uf


def OneNumOneCat(df, colNames, colTypes):
    """This function calls the statisitcal methods that generate output graphs.
    
    Args:
        df (pandas.DataFrame): The pandas dataframe that contains data columns to be analysed.
        colNames (list): The list of column names to be analysed.
        colTypes (list): The list of column types (numerical or categorical) for each column name in colName. In this case, ['Categorical','Numeric'].
    
    Returns:
        list: A list of plotly graph dictionaries.
    """
    
    df = uf.validate(df, colNames, colTypes)
    type_col, df, top_10 = nc.getTop_10(df, colNames, colTypes)
    g = [nc.cat_vs_num_recs(df, type_col)]
    df = uf.downsampleNumCat(top_10, type_col)
    # g = prob_dist(top_10,type_col) # gives error for model_name, cache_size but works for vendor, cache_size
    return (g + [nc.num_attr_spread(df, type_col), nc.box_plots(df, type_col)])   


def OneNumZeroCat(df, colNames, colTypes):
    """This function calls the statisitcal methods that generate output graphs.
    
    Args:
        df (pandas.DataFrame): The dataframe that columns to be analysed.
        colNames (list): The list of column names to be analysed.
        colTypes (list): The list of column types (numerical or categorical) for each column name in colName. In this case, ['Numeric'].
    
    Returns:
        list: A list of plotly graph dictionaries.
    """
    
    df = uf.validate(df,colNames, colTypes)
    g = [mf.numericalDescription(df, colNames), on.oneNumBar(df, colNames)]
    df = uf.downsampleNum(df, colNames)
    return (g + [on.oneNumBox(df, colNames) , on.oneNumDist(df, colNames)])


def TwoNumZeroCat(df, colNames, colTypes):
    """This function calls the statisitcal methods that generate output graphs.
    
    Args:
        df (pandas.DataFrame): The dataframe that columns to be analysed.
        colNames (list): The list of column names to be analysed.
        colTypes (list): The list of column types (numerical or categorical) for each column name in colName. In this case, ['Numeric','Numeric'].
    
    Returns:
        list: A list of plotly graph dictionaries.
    """
    
    df = uf.validate(df, colNames, colTypes)
    g = [mf.numericalDescription(df, colNames), nn.corr(df, colNames)]
    df = uf.downsampleNum(df, colNames, rows=150000)
    return (g + [nn.boxPlotComparison(df, colNames), nn.skewComparison(df, colNames), nn.skewConclusion(df, colNames), nn.scatter(df, colNames)])


def ZeroNumOneCat(df, colNames, colTypes):
    """This function calls the statisitcal methods that generate output graphs.
    
    Args:
        df (pandas.DataFrame): The dataframe that columns to be analysed.
        colNames (list): The list of column names to be analysed.
        colTypes (list): The list of column types (numerical or categorical) for each column name in colName. In this case, ['Categorical']
    
    Returns:
        list: A list of plotly graph dictionaries.
    """

    return([ mf.categoricalDescription(df, colNames), oc.charts(df, colNames)])
    

def ZeroNumTwoCat(df, colNames, colTypes):
    """This function calls the statisitcal methods that generate output graphs.

    Args:
        df (pandas.DataFrame): The dataframe that columns to be analysed.
        colNames (list): The list of column names to be analysed.
        colTypes (list): The list of column types (numerical or categorical) for each column name in colName. In this case, ['Categorical','Categorical'].

    Returns:
        list: A list of plotly graph dictionaries.
    """

    return([cc.countBarChart(df, colNames), cc.topAccounts(df, colNames), mf.categoricalDescription(df, colNames)])


def multiFeatures(df, colNames, colTypes):
    """This function calls the statisitcal methods that generate output graphs.

    Args:
        df (pandas.DataFrame): The dataframe that columns to be analysed.
        colNames (list): The list of column names to be analysed.
        colTypes (list): The list of column types (numerical or categorical) for each column name in colName.

    Returns:
        list: A list of plotly graph dictionaries.
    """
    
    colNumeric = []
    colCategorical = []
    for i in range(len(colTypes)):
        if colTypes[i] == "Numeric":
            colNumeric.append(colNames[i])
        else:
            colCategorical.append(colNames[i])
    graphs = []        
    if colNumeric:
        graphs.append(mf.numericalDescription(df, colNumeric))
        graphs.append(mf.correlationNumerical(df, colNumeric))
        
    if colCategorical:
        graphs.append(mf.correlationCategorical(df, colCategorical))
        graphs.append(mf.categoricalDescription(df, colCategorical))
    return (graphs)
    

def callDirector(df, colNames, colTypes):
    """This function calls the statistical functions based on the type of columns.

    Args:
        df (pandas.DataFrame): The dataframe that columns to be analysed.
        colNames (list): The list of column names to be analysed.
        colTypes (list): The list of column types (numerical or categorical) for each column name in colName.

    Returns:
        list: A list of plotly graph dictionaries.
    """
    
    print("Running analysis...")
    if len(colTypes) == 1:
        if colTypes[0] == 'Numeric':
            return OneNumZeroCat(df, colNames, colTypes)
        elif colTypes[0] == 'Categorical':
            return ZeroNumOneCat(df, colNames, colTypes)
        else:
            raise ValueError('Incorrect value of colTypes')
    elif len(colTypes) == 2:
        if set(colTypes) == {'Numeric'}:
            return TwoNumZeroCat(df, colNames, colTypes)
        elif set(colTypes) == {'Numeric', 'Categorical'}:
            return OneNumOneCat(df, colNames, colTypes)
        elif set(colTypes) == {'Categorical'}:
            return ZeroNumTwoCat(df, colNames, colTypes)
    else:
        return multiFeatures(df, colNames, colTypes)


if  __name__ == "__main__":
    
    try:
        ######################### GET ENV VARIABLES AND ACCESS CEPH #########################
        CEPH_S3_ACCESS_KEY = os.environ.get('CEPH_S3_ACCESS_KEY')
        CEPH_S3_SECRET_KEY = os.environ.get('CEPH_S3_SECRET_KEY')
        CEPH_S3_ENDPOINT = os.environ.get('CEPH_S3_ENDPOINT')
        CEPH_S3_BUCKET = os.environ.get('CEPH_S3_BUCKET')
        PARAMS = os.environ.get('PARAMS')
        PREFIX = os.environ.get('CEPH_S3_PREFIX')
    
        params, parserInput = uf.decodeInputJson(PARAMS)
        date = params["date"]
        outfileName = params["outfile"]
        clientKwargs = {'endpoint_url': CEPH_S3_ENDPOINT}
        s3 = s3fs.S3FileSystem(secret=CEPH_S3_SECRET_KEY, key=CEPH_S3_ACCESS_KEY, client_kwargs=clientKwargs) #Create s3 object
        
        body = uf.getOutputJson('in_progress', [], [], CEPH_S3_BUCKET, params)
        if (outfileName != 'stdout'):
            uf.writetoCeph(s3, os.path.join(CEPH_S3_BUCKET, PREFIX, outfileName), body, "Status Written to Ceph") #Write in_progess as status to Ceph
            
        ######################### CALL FUNCTIONS  #########################
        colNames, colTypes = uf.getColumnType(s3, os.path.join(CEPH_S3_BUCKET, PREFIX, 'parsers.json'), parserInput)
        df = uf.readData(s3, CEPH_S3_BUCKET, date, parserInput) #Read data
        df = uf.compressCat(df, colNames, colTypes)
        output = callDirector(df, colNames, colTypes) #Call analysis
        body = uf.getOutputJson('complete', output, [], CEPH_S3_BUCKET, params)
    
        if (outfileName != 'stdout'):
            uf.writetoCeph(s3, os.path.join(CEPH_S3_BUCKET, PREFIX, outfileName), body, "Output Written to Ceph") #Write output and complete as status to Ceph
        else:
            print("The following is the json serialized list of graphs \n")
            print(body)
            
    except OSError:
        err = {'error':str(sys.exc_info()[0]), 'message':str(sys.exc_info()[1]), 'traceback':traceback.format_exc()}
        for i, j in err.items(): print(i, j, "\n")
        
    except:
        err = [{'error':str(sys.exc_info()[0]), 'message':str(sys.exc_info()[1]), 'traceback':traceback.format_exc()}]
        for i, j in err[0].items(): print(i, j, "\n")
        body = uf.getOutputJson('errors', [], err, CEPH_S3_BUCKET, params)
        uf.writetoCeph(s3, os.path.join(CEPH_S3_BUCKET, PREFIX, outfileName), body, "Error Written to Ceph")
