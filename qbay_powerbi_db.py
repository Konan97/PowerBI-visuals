'''
This script processes fault data from Qbay First Run, filters and cleans the data, and saves it to a CSV file for further analysis. 
It imports fault data from REL3.1 and REL3.2, merges them, and categorizes the faults based on predefined categories. 
The script also handles missing values and duplicates before saving the final dataset.

author: Neehar Namjoshi
maintainer: Yuting Sun
'''
import pandas as pd
import numpy as np
import os

# 725B TT1  list
TT1_725B = [136757,
136783,
136810,
136837,
136969,
136990,
137011,
137032,
137053,
137074,
137095,
137117,
137138,
137159,
137180,
137200,
137221,
137242,
137262,
137286,
137312,
137339,
137365,
137392,
137418,
137444,
137470,
137497,
137523,
137548,
137574,
137600,
137626,
137651,
137677,
137709,
137735,
137761,
137787,
137814,
137840,
137866,
137892,
137919,
137940,
137961,
137982,
138003,
138024,
138045,
138066,
138087,
138108,
138129,
138150,
138171,
138192,
138213,
138235,
138256,
138277,
138298,
138319,
138339,
138364,
138389,
138415,
138445,
138527,
138550,
138571,
138592,
138593,
138614,
138635,
138659,
138685,
138711,
138712,
138738,
138739]

REL3_3 = [138784,
138803,
138823,
138842,
138863,
138880,
138897,
138917,
138938,
138948,
138957,
138965,
138979,
138995,
139005,
139017,
139031,
139041,
139051,
139061,
139072,
139082,
139093,
139102,
139112,
139122,
139132,
139142,
139147,
139157,
139167,
139173,
139183,
139188,
139193,
139203,
139211,
139222,
139238,
139243,
139253,
139259,
139269,
139273,
139278,
139283,
139288,
139294,
139298,
139304,
139308,
139313,
139319,
139323,
139328,
139334,
139340,
139345,
139350]
process_list = ('EOL','AirSuspension', 'FHC', 'FAS', 'VISP', 'WAE')

# Import REL3.1 Faults
directory_path = 'C:\\Users\\ysun98\\Volvo Cars\\MasterRepairman - Channel1\\REL3.1'

df = pd.read_csv(directory_path + '\\rel_3.1.csv')
print("Rel 3.1 imported successfully!")

# Import REL3.2 Faults
directory_path = 'C:\\Users\\ysun98\\Volvo Cars\\MasterRepairman - Channel1\\REL3.2'

data = []
for folder_name in os.listdir(directory_path):
    folder_path = os.path.join(directory_path, folder_name)
    if os.path.isdir(folder_path):
        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)
            tmp = pd.read_csv(file_path, skiprows=11, low_memory=False)
            tmp['VIN'] = pd.to_numeric(tmp['VIN'], errors='coerce')
            tmp['software'] = np.where(tmp['VIN'].isin(TT1_725B), 'REL7_725B_TT1', 'REL3.2')
            tmp['software'] = np.where(tmp['VIN'].isin(REL3_3), 'REL3.3', 'REL3.2')
            data.append(tmp)

df2 = pd.concat(data, ignore_index=True)
df2.drop_duplicates(subset=['VIN', 'Process', 'Phase', 'Test', 'FaultCode'], inplace=True)
df.dropna(subset=['TestTime'], axis = 0)
df2 = df2[df2['Process'].isin(process_list)]
df2.drop(['results','Unnamed: 15', 'Unnamed: 14'], inplace = True, axis = 1)

# Concat REL3.1 & REL3.2
df = pd.concat([df,df2])

# software check
print(df['software'].value_counts())

#  Clear missing/bad quality data from df and df2

df['LONGDESC'] = df['LONGDESC'].fillna(0)
df['SHORTDESC'] = df['SHORTDESC'].fillna(0)

# ECU column, week/date column, duplicates drop, keep only 6 Process/Stations 

# ECU

df['ECU'] = df['Test'].str.split(" ").str[0]


# Cal, when iFlex got new script, keep the version, drop date portion
df['script_ver'] = df['Cal'].str.split(" ").str[1]
df.rename({'Cal':'Script_version'}, inplace = True, axis = 1)

print(df['TestTime'].info())
df.dropna(subset = ['TestTime'],axis = 0, inplace = True)

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

#ToCSV
df.to_csv('C:\\Users\\ysun98\\Volvo Cars\\MasterRepairman - Channel1\\faults.csv')

print(df.shape)

#print(df['software'][df['VIN'] == 137709].value_counts())

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