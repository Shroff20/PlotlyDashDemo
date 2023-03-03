import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import matplotlib

#%% Make fake data

def get_fake_data():

    t = np.linspace(0, 10, 100)
    
    field_1 = ['A1', 'A2', 'A3']
    field_2 = ['B1', 'B2', 'B3']
    field_3 = ['C1', 'C2', 'C3']
    flagged = [True, False, False, False]
    
    fields = dict(field_1 = field_1, field_2 = field_2, field_3= field_3, flagged= flagged)
    
    df_data_1 = pd.DataFrame(index = t)
    df_data_2 = pd.DataFrame(index = t)
    
    
    
    np.random.seed(1)
    for i in range(5):
        c1 = np.random.rand()
        c2 = np.random.rand()
        df_data_1[f'case_{i}'] = np.array(c1*np.sin(c2*t + c1), dtype = 'float32')
        c1 = np.random.rand()
        c2 = np.random.rand()
        df_data_2[f'case_{i}'] = np.array(c1*np.exp(-c2*t + c1), dtype = 'float32')
    
    df_metadata = pd.DataFrame(index = df_data_1.columns)
    for field in fields:
        df_metadata[field] = np.random.choice(fields[field], len(df_metadata))

    df_metadata  = df_metadata.sort_values('flagged')
    

    return df_data_1, df_data_2, df_metadata





def make_buttons(df_metadata, field_button):

    fieldvals = set(df_metadata[field_button])
    print(fieldvals)
    buttons = []
    
    buttons.append(dict(label='all', method="update", args=[{"visible": True}]))
    
    for fieldval in fieldvals:
        I = df_metadata[field_button] == fieldval
        buttons.append(dict(label=fieldval, method="update", args=[{"visible": I}]))
    
    return buttons


#%%

def make_figure_html(df_data_1, df_data_2, df_metadata, title):
    #fig = go.Figure()
    
    subplot_titles = ('title 1', 'title 2')
    
    fig = make_subplots(rows = 1, cols = 2, subplot_titles = subplot_titles)
    
    
    cmap = plt.cm.Pastel2.colors
    hex_colors = [matplotlib.colors.to_hex(x) for x in cmap]
    print(hex_colors)
    
    
    for i,col in enumerate(df_metadata.index):
        
        is_flagged = df_metadata.loc[col, 'flagged']
        print(is_flagged)
        
        i_color = np.mod(i, len(hex_colors))
        
        if is_flagged:
            line=dict(color='blue', width=3)
        else:
            line=dict(color=hex_colors[i_color], width=2)
        
        lp = go.Scatter(x=df_data_1.index, y=df_data_1[col], mode = 'lines', name = col, line = line)
        fig.add_trace(lp, row = 1, col = 1)
        lp = go.Scatter(x=df_data_2.index, y=df_data_2[col], mode = 'lines', name = col, line = line)
        fig.add_trace(lp, row = 1, col = 2)    
    
    
    field_button = 'field_1'
    buttons =  make_buttons(df_metadata, field_button)
    
    title=go.layout.Title(text = title)

    
    updatemenus =  dict(buttons = buttons)
    fig.update_layout(updatemenus=[updatemenus], title = title,  legend={'traceorder': 'reversed'})
    
    
    fig_html = fig.to_html()
    
    return fig_html

df_data_1, df_data_2, df_metadata = get_fake_data()
print(df_data_1)
print(df_data_2)
print(df_metadata)

fig_html_1 = make_figure_html(df_data_1, df_data_2, df_metadata, 'fig1')
fig_html_2 = make_figure_html(df_data_1, df_data_2, df_metadata, 'fig1')



html_header = """
<!DOCTYPE html>
<html>
<head>
    <link rel="stylesheet" type="text/css" href="template.css">
</head>
<body>

<h1>Plots and Reports</h1>
<p>This is an example paragraph.</p>
<h1>Header</h1>
<hr>
"""



html_footer = """
</body>
</html>
"""



all_html = [html_header,  fig_html_1, fig_html_2, html_footer]
all_html = "\n".join(all_html)

with open('test1.html', 'w') as f:
    f.write(all_html)

print('done')

#%%

