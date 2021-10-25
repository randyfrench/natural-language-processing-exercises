#import libraries
import warnings
warnings.filterwarnings("ignore")

import pandas as pd
import os

# Connection
from env import host, user, password

# Acquire Data

def get_connection(db, user=user, host=host, password=password):
    '''
    This function uses my info from my env file to
    create a connection url to access the Codeup db. It takes in a string 
    name of a database as an argument
    '''
    return f'mysql+pymysql://{user}:{password}@{host}/{db}'
    

#create function to retrieve zillow data
def new_log_data():
    '''
    This function reads the Telco data from the Codeup db
    and returns a pandas DataFrame with three joined tables and all columns.
    '''
# create SQL query
    sql_query = '''
   
       SELECT * FROM logs JOIN cohorts on logs.cohort_id = cohorts.id;
       '''
    # Read in DataFrame from Codeup db.
    df = pd.read_sql(sql_query, get_connection('curriculum_logs'))
    
    return df

# this is to cache a csv file of the data from the db for a quicker read
def get_log_data():
    '''
    checks for existing csv file
    loads csv file if present
    if there is no csv file, calls new_log_data
    '''
    
    if os.path.isfile('curlog.csv'):
        
        df = pd.read_csv('curlog.csv', index_col=0)
        
    else:
        
        df = new_log_data()
        
        df.to_csv('curlog.csv')

    return df
     