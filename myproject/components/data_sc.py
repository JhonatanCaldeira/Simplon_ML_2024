import pandas as pd
import numpy as np
import os
import sys

PARENT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PARENT_DIR)
DATA_DIR = os.path.join(PARENT_DIR,'data')
DATA_FILE_IN = os.path.join(DATA_DIR,'titanic_in.csv')
DATA_FILE_OUT = os.path.join(DATA_DIR, 'titanic_out.csv')

"""
Load Titanic data into a pandas dataframe.
Return a pandas dataframe
"""
def data_load(file):
    df = pd.read_csv(file)

    return df

"""
Gets a pandas dataframe as parameter
Remove 'na' values from 'age' and 'embarked' columns
and drop the colums 'cabin', 'name', 'passengerid' and 'ticket'.
Return the dataframe
"""
def data_clean_up(df: pd.DataFrame):
    df.columns = df.columns.str.lower()
    df["age"] = df["age"].fillna(df["age"].mean())
    df = df.dropna(subset=["embarked"])
    df = df.drop(["cabin", "name", "passengerid", "ticket"], axis=1)

    return df

""" 
print the dataframe 
"""
def data_show(df: pd.DataFrame):
    print(df)

"""
Export the dataframe to a CSV file
"""
def data_write_to_csv(df: pd.DataFrame):
    df.to_csv(DATA_FILE_OUT, index=False)

if __name__ == '__main__':
    df_titanic = data_load(DATA_FILE_IN)
    df_titanic = data_clean_up(df_titanic)
    data_show(df_titanic)
    data_write_to_csv(df_titanic)

