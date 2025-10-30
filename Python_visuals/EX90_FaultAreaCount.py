"""
This program displays following tables for EX90 based on top 3 ATACQ items
 _____________________________
|Fault Area | count | percent |
|___________|_______|_________|
"""
EX90_dict = {"b727":"V536 LEFT HOOD", "b728": "V536 CENTER HOOD", "b729": "V536 RIGHT HOOD", "b730": "V536 LS A PILLAR","b731": "V536 RS A PILLAR", "b732": "V536 LS CLASS 1 FENDER", "b733": "V536 LS CLASS 2 FENDER", "b734": "V536 RS CLASS1 FENDER", "b735":"V536 RS CLASS2 FENDER", "b736":"V536 LS RAIL", "b737":"V536 RS RAIL", "b738":"V536 L1 DOOR THRESHOLD", "b739":"V536 R1 DOOR THRESHOLD", "b740":"V536 L2 DOOR THRESHOLD", "b741": "V536 R2 DOOR THRESHOLD", "b742": "V536 LS UPPER B PILLAR", "b743": "V536 LS LOWER B PILLAR", "b744":"V536 RS UPPER B PILLAR", "b745":"V536 RS LOWER B PILLAR", "b746": "V536 LS QUARTER PANEL", "b747": "V536 RS QUARTER PANEL", "b748": "V536 RECHARGE LID", "b749": "V536 L1 CLASS 1 EXTERIOR DOOR", "b750": "V536 L1 CLASS2 EXTERIOR DOOR", "b751": "V536 L2 CLASS 1 EXTERIOR DOOR", "b752": "V536 L2 CLASS 2 EXTERIOR", "b753": "V536 R1 CLASS 1 EXTERIOR DOOR", "b754": "V536 R1 CLASS 2 EXTERIOR DOOR", "b755": "V536 R2 CLASS 1 EXTERIOR DOOR", "b756":"V536 R2 CLASS 2 EXTERIOR DOOR", "b757": "V536 L1 HINGE SIDE DOOR INTERIOR", "b758": "V536 L1 BOTTOM DOOR INTERIOR", "b759": "V536 L1 DOOR INTERIOR", "b760": "V536 L2 HINGE SIDE DOOR INTERIOR", "b761":"V536 L2 BOTTOM DOOR INTERIOR", "b762":"V536 L2 DOOR INTERIOR", "b763":"V536 R1 HINGE SIDE DOOR INTERIOR", "b764":"V536 R1 BOTTOM DOOR INTERIOR", "b765":"V536 R1 DOOR INTERIOR", "b766":"V536 R2 HINGE SIDE DOOR INTERIOR", "b767":"V536 R2 BOTTOM DOOR INTERIOR", "b768":"V536 R2 DOOR INTERIOR", "b769": "V536 LS TAILGATE OPENING", "b770":"V536 RS TAILGATE OPENING", "b771":"V536 LS C PILLAR", "b772": "V536 RS C PILLAR","b773": "V536 LS D PILLAR", "b774":"V536 RS D PILLAR", "b775":"V536 LS CLASS 1 TAILGATE","b776": "V536 RS CLASS 1 TAILGATE", "b777": "V536 LS UPPER TAILGATE", "b778": "V536 RS UPPER TAILGATE", "b779": "V536 LS CLASS 2 TAILGATE", "b780":"V536 RS CLASS 2 TAILGATE", "b781":"V536 LS LOWER TAILGATE", "b782":"V536 RS LOWER TAILGATE", "b783": "V536 LS EXPOSED TAILGATE INTERIOR", "b784":"V536 RS EXPOSED TAILGATE INTERIOR"}

dataset = dataset.dropna()
dataset = dataset[dataset['Fault Area Code'].notna()]
dataset = dataset.astype({'X Coordinate':'int'})
dataset = dataset.astype({'Y Coordinate':'int'})
dataset['Fault Area Code'] = dataset['Fault Area Code'].str[0:4]
d1 = dataset.drop_duplicates(subset = ['Fault Area Code', 'Graphical Code Loc Desc', 'Rfid', 'Link Timestamp', 'X Coordinate', 'Y Coordinate'])

rfid_count = dataset['Rfid'].nunique()

fig, ax = matplotlib.pyplot.subplots(3, 1)
fig.set_figwidth(4.5)
fig.set_figheight(8.5)
fig.set_dpi(130)

#Most common: 
for i in range(3):
    ax = matplotlib.pyplot.subplot(3, 1, i+1)
    if(d1['Graphical Code Loc Desc'].value_counts().shape[0] > i):
        d3 = d1.loc[d1['Graphical Code Loc Desc'] == d1['Graphical Code Loc Desc'].value_counts().index[i]]
        d2 = d3['Fault Area Code'].value_counts().rename_axis('Fault Area Code').reset_index(name='count')
        d2['Percent'] = d2['count'] / d2['count'].sum() * 100
        d2.update(d2[['Percent']].applymap('{:,.2f}'.format))
        d2['Fault Area Code'] = d2['Fault Area Code'].str.lower()
        d2['Fault Area Code'] = d2['Fault Area Code'].apply(lambda x: EX90_dict[x] if x in EX90_dict else x)
        num_show = min(d2.shape[0], 8)
        d2 = d2.head(num_show)
        if(num_show > 0):
            ax.axis('off')
            ax.axis('tight')
            table = ax.table(cellText=d2.values, colLabels=d2.columns, loc='center', colColours=['lightgrey' for i in range(5)])
            ax.title.set_text(d1['Graphical Code Loc Desc'].value_counts().index[i])
            table.set_fontsize(9)
            table.auto_set_column_width(col=list(range(len(d2.columns))))
        else:
            temp_string = "No data available"
            matplotlib.pyplot.text(0.2, 0.5, temp_string, size=16)
            matplotlib.pyplot.axis('off')
    else:
        temp_string = "No data available"
        matplotlib.pyplot.text(0.2, 0.5, temp_string, size=16)
        matplotlib.pyplot.axis('off')

matplotlib.pyplot.tight_layout()

matplotlib.pyplot.show()