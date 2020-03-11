import plotly.graph_objects as go
import plotly.express as px
import numpy as np


def make_map(df, country_mapping):
    df = df['confirmed'].reset_index().melt(id_vars='date')
    date_max = df['date'].max()
    df = df.query("date == @date_max")
    df['iso'] = [country_mapping[country] for country in df['country_region']]
    fig = px.choropleth(df, locations='iso', color=np.log10(df['value']),
                    projection='robinson',
                    hover_data=[df['value'], df['country_region']],
                    color_continuous_scale='Reds')
    fig.update_layout(title='Click or box/lasso select on map to select a country(ies)',
            coloraxis_colorbar_tickprefix='1.e',
            dragmode='select')
    fig.update_traces(
        hovertemplate='<b>Country</b>:%{customdata[1]}<br><b>Cases</b>:%{customdata[0]}',
        )
    return fig


def make_timeplot(df):
    df_confirmed = df['confirmed']
    fig = go.Figure()
    for country in df_confirmed.columns:
        fig.add_trace(go.Scatter(x=df_confirmed.index, y=df_confirmed[country],
                                name=country, mode='markers+lines',
                                visible=False))
    fig.update_layout(title='')
    return fig



