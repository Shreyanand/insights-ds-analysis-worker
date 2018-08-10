#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 19 15:01:07 2018

@author: shrey
"""

import os
import json
import pyarrow.parquet as pq
import pandas as pd
from plotly import utils
import plotly.plotly as py
from sklearn.cluster import KMeans
from sklearn.cluster import MiniBatchKMeans
import statscomp.lttb as lttb


def decodeInputJson(PARAMS):
    """ This function decodes input variables to be used in the analysis.

    Args:
        PRARAMS(String): Json string of input parser.
    
    Returns:
        tuple: A tuple of input dictionary and parsername:columns dictionary.
    """
    
    print("Decoding input...")
    params = json.loads(PARAMS)
    parserInput = {}
    for  i in params["parsers"]:
        parserInput[i["name"]] = i["columns"]
    return params, parserInput


def getColumnType(s3, cephPath, parserInput):
    """ This function access ceph to fetch metadata and find data type of columns.

    Args:
        s3 (s3fs.S3FileSystem): The instance of ceph credentials.
        cephPath (pandas.DataFrame): The path of the file to be written.
        parserInput (dict): The dictionary with parsner name as key and column list as value. 
    
    Returns:
        list: A list of column names and column types corresponding to the all the parsers.
    """
    
    print('Getting column types...')
                
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


def readData(s3, bucket, date, parserInput):
    """This function reads the data from ceph storage.

    Args:
        s3 (s3fs.S3FileSystem): The instance of ceph credentials.
        bucket (String): The ceph storage bucket.
        data (String): The date of the parser data.
        parserInput (dict): The dictionary with parsner name as key and column list as value. 

    Returns:
        pandas.DataFrame: The dataframe extracted from the file.
    """
    
    print("Collecting data from ParquetDataset...")
    first = True
    sysId = False
    for parserName, colNames in parserInput.items():
        if 'system_id' not in colNames:
            columns = colNames + ['system_id']
        else:
            columns = colNames
            sysId = True
            
        if first:
            df = pq.ParquetDataset(os.path.join(bucket, date, parserName), filesystem=s3).read_pandas(columns=columns).to_pandas()
            first = False
        else:
            dftemp = pq.ParquetDataset(os.path.join(bucket, date, parserName), filesystem=s3).read_pandas(columns=columns).to_pandas()
            df = pd.merge(df, dftemp, on=('system_id'))
            
    if not sysId:
        df = df.drop(columns=['system_id'])
    print("Data with " + str(df.count()[0]) +  " rows collected from ParquetDataset")
    return (df)


def compressCat(df, colNames, colTypes):
    
    """This function converts type of categorical variables for efficient storage.

    Args:
        df (pandas.DataFrame): The pandas dataframe that contains data columns to be analysed.
        colNames (list): The list of column names to be analysed.
        colTypes (list): The list of column types (numerical or categorical) for each column name in colName.

    Returns:
        pandas.DataFrame: The modified datframe after compression.
    """
    
    print("Compressing categorical data with rows: " +  str(df.count()[0]))
    cat =  [colNames[i] for i in range(len(colTypes)) if colTypes[i] == "Categorical"]
    if cat: df[cat] = df[cat].astype('category')
    return df


def validate(data, colNames, colTypes):
    """This function validates the numeric attributes and drops NAN values.
    
    Args:
        data (pandas.DataFrame): The pandas dataframe that contains data columns to be analysed.
        colNames (list): The list of column names to be analysed.
        colTypes (list): The list of column types (numerical or categorical) for each column name in colName. 
    
    Returns:
        pandas.DataFrame: The modified datframe after validation.
    """
    
    numericIndices = [i for i, x in enumerate(colTypes) if x == "Numeric"]
    numericCols = [colNames[x] for i, x in enumerate(numericIndices)]
    for col in numericCols:
        data[col] = pd.to_numeric(data[col], errors='coerce')
        data = data[data[col].notnull()]
    print("Data validated with " + str(data.count()[0]) + " rows remaining")
    return data


def downsampleNum(df, colNames, rows=200000, n_clusters=100, algorithm='MiniBatchKMeans'):
    """This function downsamples numerical attributes for easy rendering on browser.
    
    Args:
        df (pandas.DataFrame): The pandas dataframe that contains data columns to be analysed.
        colNames (list): The list of column names to be analysed.
        rows (int): The number of rows to be remained after downsampling.
        n_clusters (int): The number of clusters to be formed in Kmeans. (Complexity increases linearly with this)
        algorithm (string): The algorithm to be used: either MiniBatchKMeans or lttb.
    
    Returns:
        pandas.DataFrame: The modified datframe after downsampling.
    """
    
    print('Downsampling...')
    actRows = df.count()[0]
    frac = rows / actRows
    if frac < 1:
        if len(colNames) == 1:
            mat = df[colNames].values.reshape(-1,1)
        elif len(colNames) == 2:
            if algorithm == 'lttb':
                mat = df.sort_values(by=[colNames[0]])[colNames].values
                mat = lttb.downsample(mat, n_out=rows)
                print("Downsampled using lttb from " + str(actRows) + " to " + str(rows))
                return pd.DataFrame({colNames[0]:mat[:, 0], colNames[1]: mat[:, 1]}) 
            else:
                mat = df[colNames].values

        km = MiniBatchKMeans(n_clusters=n_clusters, random_state=0)
        km.fit(mat)
        df['labels'] = km.labels_
    
        def smpl(x, **kwargs):
            frac = kwargs['frac']
            if len(x) > 1 / frac:
                return x.sample(frac = frac)
            else:
                return x 
        df = df.groupby(['labels']).apply(smpl, frac=frac)[colNames]
        print("Downsampled from " + str(actRows) + " to " + str(rows))
        return df
    else:
        print("Keeping original data with rows: " + str(actRows))
        return df


def downsampleNumCat(df, type_col, rows=200000, n_clusters=10):
    """This function downsamples numerical attributes for easy rendering on browser.
    
    Args:
        df (pandas.DataFrame): The pandas dataframe that contains data columns to be analysed.
        typ_col (dict): The dictionary of column names as key and column types as values.
        rows (int): The number of rows to be remained after downsampling.
        n_clusters (int): The number of clusters to be formed in Kmeans (Complexity increases linearly with this).
        algorithm (string): The algorithm to be used: either MiniBatchKMeans or lttb.
    
    Returns:
        pandas.DataFrame: The modified datframe after downsampling.
    """
    
    print('Downsampling...')
    actRows = df.count()[0]
    frac = rows / actRows
    num = type_col['Numeric']
    cat = type_col['Categorical']
    if frac < 1:
        def clusters(group):
            mat = group.values.reshape(-1,1)
            km = KMeans(n_clusters=n_clusters)
            km.fit(mat)
            labels = km.labels_
            return labels
        
        df['labels'] = df.groupby(cat, observed=True)[num].transform(clusters)
        
        def smpl(x, **kwargs):
            frac = kwargs['frac']
            if len(x) > 1 / frac:
                return x.sample(frac = frac)
            else:
                return x
            
        df = df.groupby([cat,'labels']).apply(smpl, frac=frac)[[cat, num]]
        print("Downsampled from " + str(actRows) + " to " + str(df.count()[0]))
        return df
    else:
        print("Keeping original data with rows: " + str(actRows))
        return df


def getOutputJson(status, data, errors, bucket, inputParams):
    """ This function gives the output json string to be stored in Ceph.

    Args:
        status (String): The status of the job: in_progress, complete, or error.
        data (dict): The dictionary associated with output graphs.
        errors (dict): The dictionary associated with output errors.
        bucket (String): The ceph storage bucket.
        inputParams (dict): The input parameters dictionary.
    
    Returns:
        String: The output json string.
    """
    
    print('Preparing output json...')
    jobDict = { 
            "metadata": {
                    "type": "plotly_graphs", 
                    "bucket": bucket,
                    "asyncJob": {
                            "status": status
                            } 
                    }, 
            "data": {
                    "date": inputParams["date"],
                    "parsers": inputParams["parsers"],
                    "graphs": data
                      },
            "errors": errors
            }
            
    return (json.dumps(jobDict, cls=utils.PlotlyJSONEncoder))


def writetoCeph(s3, path, body, log):
    """ This function writes to ceph and prints logs on stdout

    Args:
        s3 (s3fs.S3FileSystem): The instance of ceph credentials.
        path (String): The path of the file to be written.
        body: The body of the content to be written.
        log: The log to be written on stdout.
    """
    
    print('Writing to Ceph...')
    with s3.open(path, 'wb') as f:
            f.write(body.encode('utf-8'))
    print(log)


def savePng(figure, path):
    """ This function saves static png image of the plotly graph. 
    To save the image on ceph, use writetoCeph(s3, path, img, log) where
    img = py.image.get(figure, format='png')

    Args:
        figure (plotly.graph_objs.graph_objs.Figure): The plotly figure to be saved.
        path (String): The file path where the png image is to be saved.
    """
    
    print("Saving png image...")
    img = py.image.get(figure, format='png')
    with open (path, "wb") as f:
        f.write(img)
