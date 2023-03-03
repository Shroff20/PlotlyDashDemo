import numpy as np
import pandas as pd
import plotly.graph_objects as go


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

def make_figure_html(df_data, df_metadata, plot_text = 'figure header'):
    fig = go.Figure()
    for col in df_data.columns:
        lp = go.Scatter(x=df_data.index, y=df_data[col], mode = 'lines')
        fig.add_trace(lp)
    
    field_button = 'field_1'
    buttons =  make_buttons(df_metadata, field_button)
    
    title=go.layout.Title(text = plot_text)
    
    updatemenus =  dict(buttons = buttons)
    fig.update_layout(updatemenus=[updatemenus], title = title)
    
    
    fig_html = fig.to_html()
    
    return fig_html

df_data, df_metadata = get_fake_data()
print(df_data)
print(df_metadata)

fig_html_1 = make_figure_html(df_data, df_metadata, 'plot1')
fig_html_2 = make_figure_html(df_data, df_metadata, 'plot2')


html_header = """
<!DOCTYPE html>
<html>
<head>
<style>
body {background-color: powderblue;}
h1   {color: blue;}
p    {color: red;}
<link rel="stylesheet" href="tmeplate.css">

</style>
</head>
<body>
    padding: 100px;
"""

html_header = """
<!DOCTYPE html>
<html>
<head>
    <link rel="stylesheet" type="text/css" href="template.css">
</head>
<body>
"""



html_footer = """
</body>
</html>
"""


str_html1 = '<h1>Plots and Reports</h1>'
str_html2 = '<h2>Plots and Reports</h2>'


all_html = [html_header, str_html1, fig_html_1, str_html2, fig_html_2, html_footer]
all_html = "\n".join(all_html)

with open('test1.html', 'w') as f:
    f.write(all_html)

print('done')


