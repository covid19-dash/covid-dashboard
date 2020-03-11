#%%
# Preprocess data

from pycovid import pycovid
df_all = pycovid.getCovidCases()
df_all['iso'] = df_all['alpha-3']

# Sum data for provinces
group_columns = list(df_all.columns)
group_columns.remove('cases')
group_columns.remove('province_state')
df = df_all.groupby(group_columns).sum()
df_all = df.reset_index()

#%%
# Define static figure to tune its layout
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

df = df_all.query("type == 'confirmed'").query("date == '2020-03-08'")
fig1 = px.choropleth(df, locations='iso', color=np.log(df['cases']),
                    projection='robinson',
                    hover_data=[df['cases'], df['name']],
                    color_continuous_scale='Reds')
fig1.update_layout(title='Click or box/lasso select on map to select a country(ies)')
fig1.update_traces(hovertemplate='<b>Country</b>:%{customdata[1]}<br><b>New cases</b>:%{customdata[0]}')

df_confirmed = df_all.query("type =='confirmed'")

fig2 = go.Figure()
for country in df_confirmed['iso'].unique():
    df_tmp = df_confirmed.query("iso == @country")
    fig2.add_trace(go.Scatter(x=df_tmp['date'], y=np.cumsum(df_tmp['cases']), 
                              name=country, visible=False, mode='markers+lines'))

fig2.update_layout(title='')


fig1.show()
fig2.show()

#%%
# Now define figure widgets and connect click and selection events
from ipywidgets import widgets
import plotly.graph_objects as go
import numpy as np
figw1 = go.FigureWidget(fig1)
figw2 = go.FigureWidget(fig2)
map_chart = figw1.data[0]


index_dict = {fig2.data[i].name:i for i, trace in enumerate(fig2.data)}
def update_country(trace, points, selector):
    country = points.point_inds[0]
    country_name = map_chart['locations'][country] 
    with figw2.batch_update():
        figw2.data[index_dict[country_name]].visible = True
        figw2.layout.title.text = 'Evolution' 
    

def update_countries(trace, points, selector):
    countries = points.point_inds
    country_indices = [index_dict[map_chart['locations'][country]] for country in countries]
    with figw2.batch_update():
        for country_index in country_indices:
            figw2.data[country_index].visible = True
        figw2.layout.title.text = 'Evolution' 
        

#%%
map_chart.on_click(update_country)
map_chart.on_selection(update_countries)

#%%
widgets.VBox([figw1, figw2])

#%%
df_all.pivot(columns='type', values=['cases'])

#%%
df_all
