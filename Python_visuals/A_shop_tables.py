"""
This program displays the following tables.
_________________________________________
ATACQ item | Linking Workstation | count |
___________|_____________________|_______|

___________________________________________________________________________
ATACQ item | count | Polestar3 count | Polestar DPV | EX90 count| EX90 DPV |
___________|_______|_________________|______________|___________|__________|
"""

import matplotlib

stations = ['WE_GD', 'FIN_A', 'ARPR']
dataset = dataset.loc[~dataset['Linking Workstation'].isin(stations)]
options = ['RB258', 'RB292','RB403','RB245','RB402','RB410','RB401','RB411','B0540','RB251','B0102','RB09A', 'RB405','RB444', 'RB0009', 'RB400','RB446','RB100', 'B0421', 'RBB0006', 'RB291']
dataset = dataset.loc[dataset['ATACQ Item Code'].isin(options)]

dataset = dataset.dropna()
dataset = dataset.drop_duplicates(subset = ['ATACQ Item Code', 'Linking Workstation', 'ATACQ Item English Desc', 'Rfid', 'Link Timestamp', 'Main Type Description'])

rfid_count = dataset['Rfid'].nunique()
if (rfid_count == 0):
    temp_string = "No data available"
    matplotlib.pyplot.text(0.2, 0.5, temp_string, size=16)
    matplotlib.pyplot.axis('off')
else:
    fig, ax = matplotlib.pyplot.subplots(2,1)
    # table
    ax = matplotlib.pyplot.subplot(2, 1, 2)
    models = ['POLESTAR 3', 'EX90']

    # function to calculate POLESTAR 3 and EX90 seperately
    def defaultSplit(model):
        temp_df = dataset[dataset['Main Type Description'] == model]
        temp_df = temp_df['ATACQ Item English Desc'].value_counts().rename_axis('Top 10 Description').reset_index(name= model +' count')
        temp_df['Top 10 Description'] = temp_df['Top 10 Description'].str.lower().str.capitalize()
        temp_df[model + ' DPV'] = temp_df[model + ' count'] / dataset[dataset['Main Type Description'] == model]['Rfid'].nunique()
        return temp_df

    d2 = dataset['ATACQ Item English Desc'].value_counts().rename_axis('Top 10 Description').reset_index(name='count')
    d2['Top 10 Description'] = d2['Top 10 Description'].str.lower().str.capitalize()
    d2 = d2.merge(defaultSplit(models[0]), how='outer', on='Top 10 Description')
    d2 = d2.merge(defaultSplit(models[1]), how='outer', on='Top 10 Description')

    d2 = d2.head(10)
    d2.loc['Total'] = d2.sum(numeric_only=True)
    row  = d2.loc["Total"]
    row['Top 10 Description'] = "Total"
    d2.loc["Total"] = row

    d2 = d2.round(2)
    ax.axis('off')
    ax.axis('tight')
    table = ax.table(cellText=d2.values, colLabels=d2.columns, loc='center', colColours=['lightblue' for i in range(len(d2.columns))])
    table.auto_set_column_width(col=list(range(len(d2.columns))))
    table.set_fontsize(7)
    table.scale(0.4, 0.6)

    # groupby workstation table
    ax2 = matplotlib.pyplot.subplot(2, 1, 1)
    ax2.axis('off')
    ax2.axis('tight')
    dataset_workstation = dataset[['ATACQ Item English Desc', 'Rfid', 'Linking Workstation']]
    dataset_workstation = dataset_workstation.groupby(['ATACQ Item English Desc', 'Linking Workstation']).count().reset_index().rename(columns={'Rfid':'Count'}).sort_values(by='Count', ascending=False)
    dataset_workstation = dataset_workstation.head(10)
    table_workstation = ax2.table(cellText=dataset_workstation.values, colLabels=dataset_workstation.columns, loc='center', colColours=['lightblue' for i in range(len(dataset_workstation.columns))])

    table_workstation.auto_set_column_width(col=list(range(len(dataset_workstation.columns))))
    table_workstation.set_fontsize(7)

    fig.set_figwidth(7)
    fig.set_figheight(7.5)
    fig.set_dpi(175)

    fig.tight_layout()

matplotlib.pyplot.show()