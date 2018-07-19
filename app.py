import os
import sys
import traceback
import json
import pyarrow.parquet as pq
import s3fs
import itertools as it
import pandas as pd
from plotly import utils
import statscomp.OneNumOneCat as cat_num
import statscomp.OneNumZeroCat as sin_num
import statscomp.TwoNumZeroCat as num_num
import statscomp.ZeroNumOneCat as sin_cat
import statscomp.ZeroNumTwoCat as cat_cat


def readData(s3, date, parserInput):
    """This function reads the data from ceph storage.

    Args:
        s3 (s3fs.S3FileSystem): The instance of ceph credentials.
        file (String): The path of the file to be read.

    Returns:
        pandas.DataFrame: The dataframe extracted from the file.
    """
    first = True
    for parserName, colNames in parserInput.items():
        if first:
            df = pq.ParquetDataset(os.path.join(CEPH_S3_BUCKET, date, parserName), filesystem=s3).read_pandas().to_pandas()[colNames + ['system_id']]
            first = False
        else:
            dftemp = pq.ParquetDataset(os.path.join(CEPH_S3_BUCKET, date, parserName), filesystem=s3).read_pandas().to_pandas()[colNames + ['system_id']]
            df = pd.merge(df, dftemp,on=('system_id'))
    print("Data collected from ParquetDataset")
    return (df)


def callDirector(df, colNames, colTypes):
    """This function calls the statistical functions based on the type of columns.

    Args:
        df (pandas.DataFrame): The dataframe that columns to be analysed.
        colNames (list): The list of column names to be analysed.
        colTypes (list): The list of column types (numerical or categorical) for each column name in colName.

    Returns:
        String: A serialized json string of a list of json serialized plotly graphs.
    """
    if len(colTypes) == 1:
        if colTypes[0] == 'Numeric':
            return sin_num.OneNumZeroCat(df, colNames, colTypes)
        elif colTypes[0] == 'Categorical':
            return sin_cat.ZeroNumOneCat(df, colNames, colTypes)
        else:
            return ('Type Error: Incorrect data type. Data type given is not numeric or categorical')
    elif len(colTypes) == 2:
        if set(colTypes) == {'Numeric'}:
            return num_num.TwoNumZeroCat(df, colNames, colTypes)
        elif set(colTypes) == {'Numeric', 'Categorical'}:
            return cat_num.OneNumOneCat(df, colNames, colTypes)
        elif set(colTypes) == {'Categorical'}:
            return cat_cat.ZeroNumTwoCat(df, colNames, colTypes)
    else:
        raise ValueError('Incorrect value of colTypes')
    
    
def multiFeatures(df, colNames, colTypes):
    """This function generates pairs of columns and calls the statistical functions based on the type of columns.

    Args:
        df (pandas.DataFrame): The dataframe that columns to be analysed.
        colNames (list): The list of column names to be analysed.
        colTypes (list): The list of column types (numerical or categorical) for each column name in colName.

    Returns:
        String: A serialized json string of a list of json serialized plotly graphs.
    """
    if len(colTypes) > 2:
        nameType = {}
        for i in range(len(colTypes)):
            nameType[colNames[i]] = colTypes[i]
        colNamesPairs = ([list(i) for i in it.combinations(colNames, 2)])
        print(len(colNamesPairs),"Pairwise combinations")
        output = []
        for i in colNamesPairs:
            colName = i
            colType = [nameType[j] for j in colName]
            print(colName)
            output.extend(callDirector(df, colName, colType))
        return (output)
    else: 
        return (callDirector(df, colNames, colTypes))
 
    
def writetoCeph(s3, path, body, log):
    """ This function writes to ceph and prints logs on stdout
    
    Args:
        s3 (s3fs.S3FileSystem): The instance of ceph credentials.
        path (String): The path of the file to be written.
        body: The body of the content to be written
        log: The log to be written on stdout
    """
    with s3.open(path, 'wb') as f:
            f.write(body.encode('utf-8'))
    print(log)
    
    
def getColumnType(s3, cephPath, parserInput):
    """ This function access ceph to fetch metadata and find data type of columns.
    
    Args:
        s3 (s3fs.S3FileSystem): The instance of ceph credentials.
        cephPath (pandas.DataFrame): The path of the file to be written.
        parserName (String): The name of the parser to be accessed.
        colNames (list): The names of the columns whose types are required.
    
    Returns:
        list: A list of column types corresponding to the list of column names.
    """
                
    with s3.open(cephPath, 'rb') as f:
        jsonString = f.read()
    parsers = json.loads(jsonString.decode('utf-8'))['parsers']
    colNames = []
    colTypes = []
    for i in parsers:
        for parserName, colName in parserInput.items():    
            if i['name'] == parserName:
                ctypes =  i['columns']
                for j in colName:
                    for k in ctypes:
                        if j == k['name']:
                            colNames.append(j)
                            colTypes.append(k['type'])
                
    if len(colTypes) != len(colNames):
          raise NameError('Please check if passed column names match parser column names')
          
    return colNames, colTypes
    

def getOutputJson(status, data, errors, bucket, inputParams):
    jobDict = { 
            "metadata":{
                    "type":"plotly_graphs", 
                    "bucket": bucket,
                    "asyncJob":{
                            "status": status
                            } 
                    }, 
            "data":{
                    "date": inputParams["date"],
                    "parsers": inputParams["parsers"],
                    "graphs":data
                      },
            "errors":errors
            }
            
    return (json.dumps(jobDict, cls=utils.PlotlyJSONEncoder))


def decodeInputJson(PARAMS):
     params = json.loads(PARAMS)
     parserInput = {}
     for  i in params["parsers"]:
         parserInput[i["name"]] = i["columns"]
     return params, parserInput
     

if  __name__ == "__main__":
    try:
        CEPH_S3_ACCESS_KEY = os.environ.get('CEPH_S3_ACCESS_KEY')
        CEPH_S3_SECRET_KEY = os.environ.get('CEPH_S3_SECRET_KEY')
        CEPH_S3_ENDPOINT = os.environ.get('CEPH_S3_ENDPOINT')
        CEPH_S3_BUCKET = os.environ.get('CEPH_S3_BUCKET')
        PARAMS = os.environ.get('PARAMS')
        PREFIX = os.environ.get('CEPH_S3_PREFIX')
    
#        params = json.loads(PARAMS)
#        parserName = params['PARSER_NAME']
#        colNames = params['COL_NAME']
        params, parserInput = decodeInputJson(PARAMS)
        date = params["date"]
        outfileName = params["outfile"]
        clientKwargs = {'endpoint_url': CEPH_S3_ENDPOINT}
        s3 = s3fs.S3FileSystem(secret=CEPH_S3_SECRET_KEY, key=CEPH_S3_ACCESS_KEY, client_kwargs=clientKwargs)
        
        body = getOutputJson('in_progress', [], [], CEPH_S3_BUCKET, params)
        if (outfileName != 'stdout'):
            writetoCeph(s3, os.path.join(CEPH_S3_BUCKET, PREFIX, outfileName), body, "Status Written to Ceph")
    
        colNames, colTypes = getColumnType(s3, os.path.join(CEPH_S3_BUCKET, PREFIX, 'parsers.json'), parserInput)
        df = readData(s3, date, parserInput)
        output = multiFeatures(df, colNames, colTypes)
        body = getOutputJson('complete', output, [], CEPH_S3_BUCKET, params)
    
        if (outfileName != 'stdout'):
            writetoCeph(s3, os.path.join(CEPH_S3_BUCKET, PREFIX, outfileName), body, "Output Written to Ceph")
        else:
            print("The following is the json serialized list of graphs \n")
            print(body)
    except:
        err = [{'error':str(sys.exc_info()[0]), 'message':str(sys.exc_info()[1]), 'traceback':traceback.format_exc()}]
        body = getOutputJson('errors', [], err, CEPH_S3_BUCKET, params)
        writetoCeph(s3, os.path.join(CEPH_S3_BUCKET, PREFIX, outfileName), body, "Error Written to Ceph")
