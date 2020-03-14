"""
Utility functions to generate plotly figures from dataframe. Called in app.py
"""

import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import plotly.io as pio

pio.templates.default = "plotly_dark"


def make_map(df, country_mapping):
    df = df['confirmed'].reset_index().melt(id_vars='date')
    date_max = df['date'].max()
    df = df.query("date == @date_max")
    df['iso'] = [country_mapping[country] for country in df['country_region']]
    fig = px.choropleth(df, locations='iso', color=np.log10(df['value']),
                    #projection='robinson',
                    hover_data=[df['value'], df['country_region']],
                    color_continuous_scale='Plasma')
    fig.update_layout(title='Click on map to select a country',
            coloraxis_colorbar_tickprefix='1.e',
            #dragmode='select',
            margin=dict(l=0))
    fig.update_traces(
        hovertemplate='<b>Country</b>:%{customdata[1]}<br><b>Cases</b>:%{customdata[0]}',
        )
    return fig


def make_timeplot(df):
    df_confirmed = df['confirmed']
    fig = go.Figure()
    for country in df_confirmed.columns:
        fig.add_trace(go.Scatter(x=df_confirmed.index, y=df_confirmed[country],
                                name=country[1], mode='markers+lines',
                                visible=False))
    fig.update_layout(title='',
            xaxis=dict(rangeslider_visible=True,
                range=('2020-02-15', '2020-03-12'))) #TODO use a variable for max date
    fig.update_layout(
    updatemenus=[
        dict(
            type = "buttons",
            direction = "left",
            buttons=list([
                dict(
                    args=[{"visible": [False,]*len(df_confirmed.columns)}],
                    label="Reset",
                    method="update",
                ),
                dict(
                    args=["yaxis", {'type':'log'}],
                    label="log",
                    method="relayout",
                ),
                dict(
                    args=["yaxis", {'type':'linear'}],
                    label="lin",
                    method="relayout",
                ),

            ]),
            pad={"r": 10, "t": 10, "b":5},
            showactive=True,
            x=0.05,
            xanchor="left",
            y=1.35,
            yanchor="top",
            font_color='black',
        ),
    ]
)

    return fig



