import os
import json
import pyarrow.parquet as pq
import s3fs
from datetime import datetime as dtm
import statscomp.OneNumOneCat as cat_num
import statscomp.OneNumZeroCat as sin_num
import statscomp.TwoNumZeroCat as num_num
import statscomp.ZeroNumOneCat as sin_cat
import statscomp.ZeroNumTwoCat as cat_cat

def readData(file,s3):
    """This function reads the data from ceph storage.

    Args:
        file (pandas.DataFrame): The name of the file to be read.
        s3 (s3fs.S3FileSystem): The instance of ceph credentials.

    Returns:
        pandas.DataFrame: The dataframe extracted from the file.
    """
    df = pq.ParquetDataset(file, filesystem=s3).read_pandas().to_pandas()
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
        return ('Error: Incorrect number of variables')

if  __name__ == "__main__":

    CEPH_S3_ACCESS_KEY = os.environ.get('CEPH_S3_ACCESS_KEY')
    CEPH_S3_SECRET_KEY = os.environ.get('CEPH_S3_SECRET_KEY')
    CEPH_S3_ENDPOINT = os.environ.get('CEPH_S3_ENDPOINT')
    CEPH_S3_BUCKET = os.environ.get('CEPH_S3_BUCKET')
    PARAMS = os.environ.get('PARAMS')
    PREFIX = os.environ.get('CEPH_S3_PREFIX')

    params = json.loads(PARAMS)
    parserName = params['PARSER_NAME']
    colNames = params['COL_NAME']
    outfileName = params['OUTFILE_NAME']
    clientKwargs = {'endpoint_url': CEPH_S3_ENDPOINT}
    ctypes = {'account': 'Categorical','vendor': 'Categorical','cpu_count': 'Numeric','upload_time': 'Categorical','socket_count': 'Numeric',
            'system_id':'Categorical' ,'model_number': 'Categorical','cpu_speed': 'Numeric','cache_size': 'Numeric','model_name': 'Categorical'}
    colTypes = [ctypes[i] for i in  colNames]
    #fname= 'Analysis_for_' + str(colTypes) + '_at_' + str(dtm.now())

    s3 = s3fs.S3FileSystem(secret=CEPH_S3_SECRET_KEY, key=CEPH_S3_ACCESS_KEY, client_kwargs=clientKwargs)

    df = readData(os.path.join(CEPH_S3_BUCKET, parserName), s3)
    body = callDirector(df, colNames, colTypes)
    with s3.open(os.path.join(CEPH_S3_BUCKET, PREFIX, outfileName), 'wb') as f:
        f.write(body.encode('utf-8'))
    print("Graph Written to Ceph")
