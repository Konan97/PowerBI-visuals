"""
This program displays following tables for P519 based on top 3 ATACQ items
 _____________________________
|Fault Area | count | percent |
|___________|_______|_________|
"""
import matplotlib

P519_dict = {"p727":"P519 LEFT HOOD", "p728": "P519 CENTER HOOD", "p729": "P519 RIGHT HOOD", "p730": "P519 LS A PILLAR", "p731": "P519 RS A PILLAR", "p732": "P519 LS CLASS 1 FENDER", "p733": "P519 LS CLASS 2 FENDER", "p734": "P519 RS CLASS 1 FENDER", "p735":"P519 RS CLASS 2 FENDER", "p736":"P519 LS RAIL", "p737":"P519 RS RAIL", "p738":"P519 L1 DOOR THRESHOLD", "p739":"P519 R1 DOOR THRESHOLD", "p740":"P519 L2 DOOR THRESHOLD", "p741": "P519 R2 DOOR THRESHOLD", "p742": "P519 LS UPPER B PILLAR", "p743": "P519 LS LOWER B PILLAR", "p744":"P519 RS UPPER B PILLAR", "p745":"P519 RS LOWER B PILLAR", "p746": "P519 LS QUARTER PANEL", "p747": "P519 RS QUARTER PANEL", "p748": "P519 RECHARGE LID", "p749": "P519 L1 CLASS 1 EXTERIOR DOOR", "p750": "P519 L1 CLASS 2 EXTERIOR DOOR", "p751": "P519 L2 CLASS 1 EXTERIOR DOOR", "p752": "P519 L2 CLASS 2 EXTERIOR DOOR", "p753": "P519 R1 CLASS 1 EXTERIOR DOOR", "p754": "P519 R1 CLASS 2 EXTERIOR DOOR", "p755": "P519 R2 CLASS 1 EXTERIOR DOOR", "p756":"P519 R2 CLASS 2 EXTERIOR DOOR", "p757": "P519 L1 HINGE SIDE DOOR INTERIOR", "p758": "P519 L1 BOTTOM DOOR INTERIOR", "p759": "P519 L1 DOOR INTERIOR", "p760": "P519 L2 HINGE SIDE DOOR INTERIOR", "p761":"P519 L2 BOTTOM DOOR INTERIOR", "p762":"P519 L2 DOOR INTERIOR", "p763":"P519 R1 HINGE SIDE DOOR INTERIOR", "p764":"P519 R1 BOTTOM DOOR INTERIOR", "p765":"P519 R1 DOOR INTERIOR", "p766":"P519 R2 HINGE SIDE DOOR INTERIOR", "p767":"P519 R2 BOTTOM DOOR INTERIOR", "p768":"P519 R2 DOOR INTERIOR", "p769": "P519 LS TAILGATE OPENING", "p770":"P519 RS TAILGATE OPENING", "p771":"P519 LS C PILLAR", "p772": "P519 RS C PILLAR"}

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
        d2['Fault Area Code'] = d2['Fault Area Code'].apply(lambda x: P519_dict[x] if x in P519_dict else x)
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