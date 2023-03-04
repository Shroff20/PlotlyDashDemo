import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import matplotlib

import datetime


import plotly.io as pio
pio.renderers.default='browser'




#%% Make fake data

def get_random_day():
    ryear = int(np.random.rand()*20 + 2000)
    rmonth = int(np.random.rand()*11+1)
    rday = int(np.random.rand()*27+1)
    date = datetime.date(ryear, rmonth, rday)
    
    return date




def get_fake_data():

    t = np.linspace(0, 10, 100)
    
    field_1 = [f'A_{i}' for i in range(100)]
    field_2 = ['B1', 'B2', 'B3']
    field_3 = ['C1', 'C2', 'C3']
    
    date = [get_random_day() for x in range(100)]
    
    
    flagged = [True, False, False, False]
    
    fields = dict(field_1 = field_1, field_2 = field_2, field_3= field_3, flagged= flagged, date = date)
    
    df_data_1 = pd.DataFrame(index = t)
    df_data_2 = pd.DataFrame(index = t)
    
    
    np.random.seed(1)
    for i in range(500):
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
    
    df_metadata.index = df_metadata.index + "_" + df_metadata['date'].astype(str)
    df_data_1.columns = df_metadata.index 
    df_data_2.columns = df_metadata.index 

    return df_data_1, df_data_2, df_metadata





def make_buttons(df_metadata, field_button, trace_cases):

    fieldvals = set(df_metadata[field_button])
    
    buttons = []
    buttons.append(dict(label='all', method="update", args=[{"visible": True}]))
    
    for fieldval in fieldvals:
        
        filtered_cases = list(df_metadata[df_metadata[field_button] == fieldval].index)
        filtered_cases.append('always_show')

        #I = df_metadata[field_button] == fieldval
        I = [x in filtered_cases for x in  trace_cases]
        buttons.append(dict(label=fieldval, method="update", args=[{"visible": I}]))
    
    return buttons


#%%

def make_figure_html(df_data_1, df_data_2, df_metadata, title):
    #fig = go.Figure()
    
    subplot_titles = ('title 1', 'title 2')
    
    dt = np.max(df_metadata['date'])-np.min(df_metadata['date'])
    date_range = (np.min(df_metadata['date'])- + dt/20  , np.max(df_metadata['date']) + dt/20 )
    
    fig = make_subplots(rows = 2, cols = 2, subplot_titles = subplot_titles, 
                        row_heights  = (1, .1), vertical_spacing  = .2, specs = [[{}, {}], [{'colspan': 2}, None]])
    
    trace_cases = []



    cmap = plt.cm.Pastel2.colors
    hex_colors = [matplotlib.colors.to_hex(x) for x in cmap]


    for i,col in enumerate(df_metadata.index):
        
        is_flagged = df_metadata.loc[col, 'flagged']
        
        i_color = np.mod(i, len(hex_colors))
        
        if is_flagged:
            line=dict(color='blue', width=3)
        else:
            line=dict(color=hex_colors[i_color], width=2)
        
        lp = go.Scatter(x=df_data_1.index, y=df_data_1[col], mode = 'lines', name = col, line = line)
        fig.add_trace(lp, row = 1, col = 1)
        trace_cases.append(col)
        lp = go.Scatter(x=df_data_2.index, y=df_data_2[col], mode = 'lines', name = col, line = line)
        fig.add_trace(lp, row = 1, col = 2)    
        trace_cases.append(col)
        marker=dict(color='red', size=20)
 
        lp = go.Scatter(x=[df_metadata.loc[col, 'date']], y=[0], mode = 'markers', marker = marker, showlegend=False)
        fig.add_trace(lp, row = 2, col = 1)    
        trace_cases.append(col)
    fig.update_layout(yaxis3 = dict(visible=False), xaxis3=dict(range=date_range))
        
        
# fig.update_layout(plot_bgcolor = "white")
# fig.update_layout(showlegend=False, height = 200)
    

    lp = go.Scatter(x=date_range, y=(0,0), mode = 'lines', line = dict(color='black', width=2), showlegend=False)
    fig.add_trace(lp, row = 2,col = 1)   
    trace_cases.append('always_show')
    
    
    field_button = 'field_1'
    buttons =  make_buttons(df_metadata, field_button, trace_cases)

    
    updatemenus =  dict(buttons = buttons)
    fig.update_layout(updatemenus=[updatemenus], title = title,  legend={'traceorder': 'reversed'}, template="plotly_white")
        
    fig.show()
    title=go.layout.Title(text = title)
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


            
            
# fig = make_subplots()

# date_range = (np.min(df_metadata['date']), np.max(df_metadata['date']))

# marker=dict(color='red', size=20)
# line=dict(color='black', width=2)
# lp = go.Scatter(x=date_range, y=(0,0), mode = 'lines', line = line)
# fig.add_trace(lp)    
# lp = go.Scatter(x=df_metadata['date'], y=np.zeros(len(df_metadata)), mode = 'markers', marker = marker)
# fig.add_trace(lp)    
# fig.update_yaxes(visible=False)
# fig.update_layout(plot_bgcolor = "white")
# fig.update_layout(showlegend=False, height = 200)
# fig.show()