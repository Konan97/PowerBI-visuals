import pandas as pd

df_faults = pd.read_csv('C:\\Users\\ysun98\\Volvo Cars\\MasterRepairman - Channel1\\faults.csv', low_memory=False)
df_cars = pd.read_csv('C:\\Users\\ysun98\\Volvo Cars\\MasterRepairman - Channel1\\cars.csv', low_memory=False)
# print(df_faults.head())
# print(df_cars.head())

df_combine = pd.merge(df_faults, df_cars, left_on='VIN', right_on='Mix Number', how='right')
print(df_combine.columns)
df_grouped = df_combine.groupby(['VIN']).apply(lambda x: x)
print(df_grouped.head())

df_grouped.to_csv('C:\\Users\\ysun98\\Volvo Cars\\MasterRepairman - Channel1\\output.csv')