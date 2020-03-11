import plotly.graph_objects as go
import plotly.express as px
import numpy as np


def make_map(df_all):
    df = df_all.query("type == 'confirmed'").query("date == '2020-03-08'")
    fig = px.choropleth(df, locations='iso', color=np.log(df['cases']),
                    projection='robinson',
                    hover_data=[df['cases'], df['name']],
                    color_continuous_scale='Reds')
    fig.update_layout(title='Click or box/lasso select on map to select a country(ies)')
    fig.update_traces(hovertemplate='<b>Country</b>:%{customdata[1]}<br><b>New cases</b>:%{customdata[0]}')
    return fig


def make_timeplot(df):
    df_confirmed = df['confirmed']
    fig = go.Figure()
    for country in df_confirmed.columns:
        fig.add_trace(go.Scatter(x=df_confirmed.index, y=df_confirmed[country],
                                name=country, mode='markers+lines'))
    fig.update_layout(title='')
    return fig



