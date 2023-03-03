import numpy as np
import pandas as pd
import plotly 
import plotly.graph_objects as go
import plotly.express as px
import os



#%% Make fake data

def get_fake_data():

    t = np.linspace(0, 10, 100)
    
    field_1 = ['A1', 'A2', 'A3']
    field_2 = ['B1', 'B2', 'B3']
    field_3 = ['C1', 'C2', 'C3']
    fields = dict(field_1 = field_1, field_2 = field_2, field_3= field_3)
    
    df_data = pd.DataFrame(index = t)
    np.random.seed(1)
    for i in range(20):
        c1 = np.random.rand()
        c2 = np.random.rand()
        df_data[f'case_{i}'] = c1*np.sin(c2*t + c1)
    
    df_metadata = pd.DataFrame(index = df_data.columns)
    for field in fields:
        df_metadata[field] = np.random.choice(fields[field], len(df_metadata))

    return df_data, df_metadata

df_data, df_metadata = get_fake_data()


print(df_data)
print(df_metadata)

#%%

fig = go.Figure()

for col in df_data.columns:
    lp = go.Scatter(x=df_data.index, y=df_data[col], mode = 'lines')
    fig.add_trace(lp)


field_button = 'field_1'



fieldvals = set(df_metadata[field_button])
print(fieldvals)
buttons = []

for fieldval in fieldvals:
    I = df_metadata[field_button] == fieldval
    buttons.append(dict(label=fieldval, method="update", args=[{"visible": I}]))


updatemenus =  dict(buttons = buttons)
fig.update_layout(updatemenus=[updatemenus])

html_txt = fig.to_html('test2.html')

with open('test1.html', 'w') as f:
    f.write(html_txt)

print('done')