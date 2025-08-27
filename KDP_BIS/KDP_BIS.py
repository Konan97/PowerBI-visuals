import snowflake.snowpark as snowpark
from snowflake.snowpark.functions import col
 
import pandas as pd
import numpy as np
import re
from datetime import datetime, timedelta
from snowflake.snowpark import Session
import tomllib

def getConnection():
    try:
        with open('connections.toml', 'rb') as f:
            connections = tomllib.load(f)
        print(connections)
    except FileNotFoundError:
        print("connections.toml file not found.")

    connection_parameters = {
        "account": connections['snowflake_account']['account'],
        "user": connections['snowflake_account']['user'],
        "role": connections['snowflake_account']['role'],
        "database": connections['snowflake_account']['database'],
        "schema": connections['snowflake_account']['schema'],
        "warehouse": connections['snowflake_account']['warehouse'],
        "authenticator": connections['snowflake_account']['authenticator']
    }
    session = Session.builder.configs(connection_parameters).create()
    return session

def getTable(session: snowpark.Session):
    tableName = 'MANUFACTURING_ENTERPRISE_DATA_PRODUCTS.BIS_ITEMS.BIS_ITEM_DETAILS'
    # Filter for informative columns and SN read data rows
    filter_cols = ['"_id_site"', '"bartender_xml_identifier"', '"bis_item"', '"version"', '"model"',
                   '"text_type"', '"text_steering"', '"relative_position"', 
                   '"bis_item_steering_text_length"']
    dataframe = session.table(tableName)\
        .filter(
            #(col('"Attribute"').like('%SN SWDL%')) &
            (col('"bis_item"').isNotNull()) &
            (col('"bartender_xml_identifier"').like('%$%')) &
            (col('"_id_site"') == 'VCCH')
        ).select(filter_cols)
 
    # convert to Pandas (modin) for analysis 
    data = dataframe.to_pandas()
    print(data.head())
    return session.create_dataframe(data=data)



def KDP_from_csv(directory_path):
    """Helper function to read a CSV file and return a DataFrame."""
    KDP_df = pd.read_csv(directory_path, skiprows=8, low_memory=False)
    # KDP_to_BIS = {'Part Number': 'Text', 'Part type': 'Rel pos', 'ECU': 'bartender_xml_identifier', 'bartender_xml_identifier': 'bis_item'}
    KDP_df['Part Number'] = KDP_df['Part Number'].astype(str)
    return KDP_df

if __name__ == "__main__":
    directory_path = '"C:\Users\YSUN98\OneDrive - Volvo Cars\Desktop\KDP_BIS\Preserie-725B_PP11CH(Preserie-725B_PP11CH).csv"'
    KDP_df = KDP_from_csv(directory_path)
    session = getConnection()
    getTable(session)
    session.close()