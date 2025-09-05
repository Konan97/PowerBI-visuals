import snowflake.snowpark as snowpark
from snowflake.snowpark.functions import col
 
import pandas as pd
import numpy as np
import re
from datetime import datetime, timedelta
from snowflake.snowpark import Session
import tomllib

class Comparison(object):
    def __init__(self, directory_path, user_input):
        self.directory_path = directory_path
        self.user_input = user_input
        self.KDP_df = pd.DataFrame()
        self.BIS_df = pd.DataFrame()
        self.output_columns = ['Item', 'Item Type', 'Version', 'Model', 'No', 'Type', 'Text',
        'Base file', 'Rel pos', 'Length', 'Nr.', 'Cd', 'Condition',
        'Descr. PML', 'Neg', 'Base file condition', 'Pop Base file',
        'Starting position', 'Length.1', 'Valid from', 'Valid to',
        'Plass.week from', 'To plass.week', 'Shift in', 'Shift out']
        
        self.SW_partNumOrder = {'SWS1': 27, 'SWE1': 39, 'SWLM': 75, 'SWL2': 84, 'SWL3': 93, 'SWL4': 102, 'SWP2': 138, 'SWM1': 30,
        'SWTV': 12, 'SWZ1': 17, 'SWP1': 129, 'SWBL': 21, 'SWBT': 48, 'SWFD': 183, 'SWCE': 66, 'SWP3': 147,
        'SWP4': 156, 'SWK1': 12, 'SWK2': 12, 'SWK3': 12, 'SWK4': 12, 'SWK5': 12, 'SWK6': 12,
        'SWP5': 165}

    def getConnection(self, user_input):
        connections = {}
        try:
            with open('connections.toml', 'rb') as f:
                connections = tomllib.load(f)
            print(connections)
        except FileNotFoundError:
            print("connections.toml file not found.")

        connection_parameters = {
            "account": connections['snowflake_account']['account'],
            "user": user_input,
            "role": connections['snowflake_account']['role'],
            "database": connections['snowflake_account']['database'],
            "schema": connections['snowflake_account']['schema'],
            "warehouse": connections['snowflake_account']['warehouse'],
            "authenticator": connections['snowflake_account']['authenticator']
        }
        session = Session.builder.configs(connection_parameters).create()
        return session

    def getTable(self, session: snowpark.Session):
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
        return data



    def KDP_from_csv(self, directory_path):
        """Helper function to read a CSV file and return a DataFrame."""
        tmp_df = pd.read_excel(directory_path, skiprows=8)
        # KDP_to_BIS = {'Part Number': 'Text', 'Part type': 'Rel pos', 'ECU': 'bartender_xml_identifier', 'bartender_xml_identifier': 'bis_item'}
        # modify KDP columns
        tmp_df = tmp_df[~tmp_df['Part Number'].isin([32218512, 32375204])]  # remove rows with Part Number 32218512 or 32375204
        tmp_df['Part Number'] = tmp_df['Part Number'].astype(str)

        return tmp_df

    def BIS_from_snowflake(self, user_input):
        session = self.getConnection(user_input)
        tmp_df = self.getTable(session)
        tmp_df['text_steering'] = tmp_df['text_steering'].str.replace(' ', '')
        session.close()
        return tmp_df

    def create_new_row(self, row):
        # Mapping dictionary from KDP to BIS
        KDP_to_BIS = {'Part Number': 'Text', 'Part type': 'Rel pos', 'ECU': 'bartender_xml_identifier', 'bartender_xml_identifier': 'bis_item'}
        new_row = {'Version': 1, 'Model': 7, 'Neg': False, 'Base file condition': '', 'Pop Base file': '',
        'Starting position': 0, 'Length.1': 0, 'Plass.week from': 190001, 'To plass.week': 210001, 'Shift in': '', 'Shift out': ''}
        for col_name in self.KDP_df.columns: # Iterate through original KDP columns to check mapping
            if col_name in KDP_to_BIS:
            # Access the value from the current row being processed by apply
                col_value = row[col_name]
            # print(col_value)
                if col_value in self.SW_partNumOrder:
                    new_row[KDP_to_BIS[col_name]] = self.SW_partNumOrder[col_value]
                elif col_name == 'ECU':
                    # Need to handle potential NaN values in 'ECU' column
                    if pd.notna(col_value):
                        # Use a conditional check to avoid error if the key doesn't exist
                        new_row['ECU'] = col_value
                        if "$" + str(col_value) in self.BIS_df['bartender_xml_identifier'].values:
                            new_row[KDP_to_BIS[KDP_to_BIS[col_name]]] = self.BIS_df[self.BIS_df['bartender_xml_identifier'] == "$" + str(col_value)]['bis_item'].iloc[0]
                        else:
                            print(f"Warning: bartender_xml_identifier for ECU '{col_value}' not found in BIS_df.")
                    else:
                        print("Warning: NaN value in ECU column, cannot map to bartender_xml_identifier.")
                else:
                    new_row[KDP_to_BIS[col_name]] = col_value

        return new_row

    def run_process(self):
        # imported KDP file
        self.KDP_df = self.KDP_from_csv(self.directory_path)
        self.BIS_df = self.BIS_from_snowflake(self.user_input)
        # Process
        # 'Part Number' from the filtered KDP dataframe is not in the 'text_steering' column of the BIS dataframe.
        temp = self.KDP_df[~self.KDP_df.apply(lambda row: row['Part Number'] in self.BIS_df[self.BIS_df['bartender_xml_identifier'] == "$" + str(row['ECU'])]['text_steering'].values, axis=1)]
        #print(temp.head(20))
        new_rows_list = temp.apply(lambda row: self.create_new_row(row), axis=1).tolist()
        new_rows_df = pd.DataFrame(new_rows_list)
        print(new_rows_df.head(20))

        # output to CSV
        self.directory_path = re.sub(r'\.xlsx?$', '_output.csv', self.directory_path)
        new_rows_df.to_csv(self.directory_path)
        return self.directory_path
