'''
This script processes fault data from Qbay First Run, filters and cleans the data, and saves it to a CSV file for further analysis. 
It imports fault data from REL3.1 and REL3.2, merges them, and categorizes the faults based on predefined categories. 
The script also handles missing values and duplicates before saving the final dataset.

author: Neehar Namjoshi
maintainer: Yuting Sun
'''
'''activate the virtual environment before running this script
Pandas and numpy libraries are located inside the virtual environment
`.venv\Scripts\activate` to activate the virtual environment
`pip install pandas numpy` if you need to install the libraries'''

import pandas as pd
import numpy as np
import os
import project_mix, ECU_list


process_list = ('EOL','AirSuspension', 'FHC', 'FAS', 'VISP', 'WAE', 'ReFlash')

# Import REL3.1 Faults
# directory_path = 'C:\\Users\\ysun98\\Volvo Cars\\MasterRepairman - Channel1\\REL3.1'

# df = pd.read_csv(directory_path + '\\rel_3.1.csv')
# print("Rel 3.1 imported successfully!")

# Import REL3.2 Faults
# directory_path = 'C:\\Users\\ysun98\\Volvo Cars\\MasterRepairman - Channel1\\REL3.2'

def dataframe_from_csv(directory_path):
    """Helper function to read a CSV file and return a DataFrame."""
    SW_version = directory_path.split('\\')[-1]
    data = []
    for folder_name in os.listdir(directory_path):
        folder_path = os.path.join(directory_path, folder_name)
        if os.path.isdir(folder_path):
            for file_name in os.listdir(folder_path):
                file_path = os.path.join(folder_path, file_name)
                tmp = pd.read_csv(file_path, skiprows=11, low_memory=False)
                tmp['VIN'] = pd.to_numeric(tmp['VIN'], errors='coerce')
                tmp['software'] = np.where(tmp['VIN'].isin(project_mix.TT1_725B), '725B_TT1', SW_version)
                tmp['software'] = np.where(tmp['VIN'].isin(project_mix.REL3_3), 'REL3.3', tmp['software'])
                tmp['software'] = np.where(tmp['VIN'].isin(project_mix.TT2_725B), '725B_TT2', tmp['software'])
                data.append(tmp)
    data = pd.concat(data, ignore_index=True)
    return data

data3_2 = dataframe_from_csv('C:\\Users\\ysun98\\Volvo Cars\\MasterRepairman - Channel1\\REL3.2')
data3_3 = dataframe_from_csv('C:\\Users\\ysun98\\Volvo Cars\\MasterRepairman - Channel1\\REL3.3')

result_df = pd.concat([data3_2, data3_3], ignore_index=True)
#print(df2[['VIN','TestTime']][(df2['VIN'] == 139120) & (df2['Process'] == 'EOL')]).value_counts()
result_df.dropna(subset=['TestTime'], axis = 0, inplace = True)
result_df.drop_duplicates(subset=['VIN', 'Process', 'Phase', 'Test', 'FaultCode', 'TestTime'], inplace=True)

# df.dropna(subset=['TestTime'], axis = 0)
result_df = result_df[result_df['Process'].isin(process_list)]
result_df.drop(['results','Unnamed: 15'], inplace = True, axis = 1)
#df2 = df2.sort_values(by = ['VIN'], ascending = True)

# Concat REL3.1 & REL3.2
# df = pd.concat([df,df2])
df = result_df
# software check
print(df['software'].value_counts())
#print(df['VIN'][df['software'] == 'REL3.3'].value_counts())
#print(df['VIN'][df['software'] == 'REL3.2'].value_counts())

#  Clear missing/bad quality data from df and df2

df['LONGDESC'] = df['LONGDESC'].fillna(0)
df['SHORTDESC'] = df['SHORTDESC'].fillna(0)

# ECU column, week/date column, duplicates drop, keep only 6 Process/Stations 

#df['ECU'] = df['Test'].str.split(" ").str[0] # check ECUs from the list
df['ECU'] = df['Test'].apply(lambda ecu: next((i for i in ecu.split(" ") if i in ECU_list.ECUs), None))                                                               
df['Solution'] = df['ECU'].map(ECU_list.ECUs)

# Cal, when iFlex got new script, keep the version, drop date portion
df['script_ver'] = df['Cal'].str.split(" ").str[1]
df.rename({'Cal':'Script_version'}, inplace = True, axis = 1)
#df['TestTime'] = np.where(df['software'] == 'REL3.3'),'2024-04-17',df['TestTime'])
#df.dropna(subset = ['TestTime'],axis = 0, inplace = True)

# Mapping/Grouping ECU
catLPC = ['LPC', 'IPDA', 'PDS', 'PDM', 'IRPA', 'RPDS', 'RPDM', 'NFCA', 'IDDA', 'DDS', 'DDM', 'IRDA', 'RDDS', 'RDDM', 'ADSS', 'POT', 'TRM', 'DLPR', 'DLPL', 
           'HCMR', 'HCML', 'GRCM','FMDM','BBS','ADWM','WMM','IFA','IIPA','ITA','TTLL','BTLL','TTLR','BTLR','RLSM','IRMM','SUS','HUS','IRA','OHLC','OHRR','OHTL',
           'OHTR','OHC','OHRL','LCSP']
catVCU = ['VCU','HPA','HIA','HIB','VESB','SGA','LPA','VESA','VESB','SRCF','SRCB','SRCR','SRCL','DMCD','DMCI','FLCW']
catVCU_sub_1 = ['FGWM','BMSA','IHFA','ELAC','HVVB','ACCA','EXVB','BCMA','FLR','FSRL','FSRR','PSCM','SWM']
catVCU_sub_2 = ['DGWM', 'DESM', 'SUM','ASWM','RML','CCMB','SCMD','PSMD','IHRA','OCPR','RSRL','SRSM','OWS','PSMR','SHFL','SHRL','RCSM','HBMF','HUSI','AAC','APMS',
                'SWSL','SWSR','HOD','AQGSM']
catVCU_sub_3 = ['PGWM','PESM','ADPU','MSM','HLCM','HVBM','SHRR','SHFR','TVRR','TVRL','PSMP','SCMP','PDD','BPD','RSRR','SLCM','CRSM','RDCM','HBMR']
catHIC = ['VESC', 'HIC', 'HPB', 'FLL', 'FLCL', 'LRBL', 'LRBR', 'SRSR', 'PSCM', 'RBCM']
catBPD_PS = ['BPD']
catPPD_PS = ['PPD']
catHIC_1 = ['HIC','SRSR','PSCM','RBCM']
catHPB_1 = ['HPB','FLCL','LRBL','LRBR']
catDHU = ['DHU','DHUH','DHUM','CSD','HUD','DIMD','GCCC','AUD','WPC']
catTCAM = ['TCAM','TCA','PAK','UWB','BMS']
catFIOC = ['FIOC','HVCH','CRVM','CPED','BCPM','CCPM','CCVM','ASSM']
catmisc = ['RCSP','PSRL','FDM','SCRL','PSRR','SCRR']



print(df.columns)
#print(df['VIN'][df['software'] == 'REL3.3'].value_counts())

#ToCSV
df.to_csv('C:\\Users\\ysun98\\Volvo Cars\\MasterRepairman - Channel1\\faults.csv')

print(df.shape)

print("Pre-processing Succesful!")



# all_categories = catLPC + catVCU + catVCU_sub_1 + catVCU_sub_2 + catVCU_sub_3 + catHIC + catBPD_PS + catPPD_PS + catHIC_1 + catHPB_1 + catDHU + catTCAM + catFIOC + catmisc

# # Filter the DataFrame to include only faults in the defined categories
# filtered_df = df[df['ECU'].isin(all_categories)]

# # Group by VIN and Fault, and count occurrences
# grouped_df = filtered_df.groupby(['VIN']).filter(lambda x: len(x) > 2)

# # Combine the grouped DataFrame with the original DataFrame to include rows with 2 or fewer occurrences
# result_df = pd.concat([grouped_df, df[~df['VIN'].isin(grouped_df['VIN'])]])

# print(result_df)
# print(result_df.shape)
# print(df.shape)



# # To Excel
# #df_3_1 = df_tot[df_tot['software'] == 'Rel 3.1']
# #df_3_2 = df_tot[df_tot['software'] == 'Rel 3.2']

# #df_3_1.to_csv('/content/drive/MyDrive/software/df_3-1.csv')
# #df_3_2.to_csv('/content/drive/MyDrive/software/df_3-2.csv')

# from datetime import date
# today = date.today()
# format_date = today.strftime("%m-%d")

## file_path = '/content/drive/MyDrive/software/'
## file_name = f'df_tot_{format_date}.csv'
## df_tot.to_csv(file_path + file_name)