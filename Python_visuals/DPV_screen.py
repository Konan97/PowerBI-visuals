"""Paint in: data"""
import pandas as pd
import matplotlib.pyplot as plt

if (dataset.shape[0] == 0):
    temp_string = "No data"
    plt.text(0.2, 0.5, temp_string, size=14)
else:
    dataset['total'] = dataset.shape[0]
    dataset = dataset[['total']]
    dataset.drop_duplicates(inplace=True)
        
    table = plt.table(cellText=dataset.values, cellLoc='center', loc='center')
    # remove cell edge
    for c in table.get_children():
        c.set_edgecolor('none')
    table.set_fontsize(20)
    table.auto_set_column_width(col=list(range(len(dataset.columns))))
    table.scale(1, 5)

plt.axis('off')
plt.show() 

"""Work deck + DPV"""
import pandas as pd
import matplotlib.pyplot as plt

if (dataset.shape[0] == 0):
    temp_string = "No data"
    plt.text(0.2, 0.5, temp_string, size=14)
else:
    maxTime = dataset['dpvEventTimestamp'].max()
    dataset = dataset[dataset['dpvEventTimestamp'] == maxTime]
    dataset = dataset[["registrationPointDescription", "dpvScore", "dpvTarget"]]
    # round to 2 digits
    dataset['dpvScore'] = dataset['dpvScore'].apply(lambda x: round(x, 2))

    # add cell color
    bgColor = [['white', 'white']]

    if dataset.values[0][1] > dataset.values[0][2]:
        bgColor[0][1] = 'tomato'
    else:
        bgColor[0][1] = 'springgreen'

    dataset = dataset[["registrationPointDescription","dpvScore"]]

    table = plt.table(cellText=dataset.values, cellColours=bgColor, loc='center')
    # remove cell edge
    for c in table.get_children():
        c.set_edgecolor('none')

    table.set_fontsize(20)
    table.auto_set_column_width(col=list(range(len(dataset.columns))))
    table.scale(1, 5)
plt.axis('off')
plt.show()


"""FTT"""
import pandas as pd
import matplotlib.pyplot as plt

if (dataset.shape[0] == 0):
    temp_string = "No data"
    plt.text(0.2, 0.5, temp_string, size=14)
else:
    maxTime = dataset['fttEventTimestamp'].max()
    dataset = dataset[dataset['fttEventTimestamp'] == maxTime]
    dataset = dataset[["fttPercentage", "fttTarget"]]
    # round to 2 digits
    dataset['fttPercentage'] = dataset['fttPercentage'].apply(lambda x: round(x, 2))

    # add cell color
    bgColor = [['white']]

    # [[actual, target]]
    if dataset.values[0][0] < dataset.values[0][1]:
        bgColor[0][0] = 'tomato'
    else:
        bgColor[0][0] = 'springgreen'

    dataset = dataset[['fttPercentage']]
        
    table = plt.table(cellText=dataset.values, cellColours=bgColor, cellLoc='center', loc='center')
    # remove cell edge
    for c in table.get_children():
        c.set_edgecolor('none')
    table.set_fontsize(20)
    table.auto_set_column_width(col=list(range(len(dataset.columns))))
    table.scale(1, 5)
plt.axis('off')
plt.show() 