"""
Utility functions to generate plotly figures from dataframe. Called in app.py
"""

import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import pandas as pd
import plotly.io as pio
from plotly.validators.scatter.marker import SymbolValidator

from data_input import normalize_by_population

pio.templates.default = "plotly_white"

FIRST_LINE_HEIGHT = 600

LABEL_FONT_SIZE = 18


def make_map(df, df_fatalities, df_recovered):
    """
    Build figure with map of total number of cases

    Parameters
    ----------
    df: pandas DataFrame
        Our cases to plot
    pop: pandas DataFrame
        The population, used to normalize
    """
    normalized_values = normalize_by_population(df)
    # Plot per Million individual
    normalized_values *= 1e6
    hovertemplate = ('<b>Country</b>:%{customdata[0]}<br>' +
                     '<b>Active cases per million</b>: %{customdata[1]:.1f}<br>' +
                     '<b>Active cases</b>: %{customdata[2]}<br>' +
                     '<b>Fatalities</b>: %{customdata[3]}<br>' +
                     '<b>Recovered</b>: %{customdata[4]}' 
                     )
    fig = px.choropleth(df, locations='iso',
                    color=np.log10(normalized_values),
                    custom_data=[df['country_region'], normalized_values,
                                 df['value'], df_fatalities['value'],
                                 df_recovered['value']],
                    color_continuous_scale='Plasma_r',
                    labels={'color': 'Active<br>cases<br>per<br>Million'})

    fig.update_geos(lataxis_range=[-90, 90], lonaxis_range=[-160, 180])
    fig.update_layout(title='Click on map to add/remove a country',
            coloraxis_colorbar_tickprefix='1.e',
            coloraxis_colorbar_len=0.6,
            coloraxis_colorbar_title_font_size=LABEL_FONT_SIZE,
            margin=dict(l=0.03, r=0, b=0),
            height=FIRST_LINE_HEIGHT,
            geo_projection_scale=1.26)
    fig.update_traces(
            hovertemplate=hovertemplate,
        )
    return fig


def make_timeplot(df_measure, df_prediction):
    """
    Build figure showing evolution of number of cases vs. time for all countries.
    The visibility of traces is set to 0 so that the interactive app will
    toggle the visibility.

    Parameters
    ----------
    df_measure: pandas DataFrame
        DataFrame of measured cases, created by :func:`data_input.get_data`, of wide format.

    df_prediction: pandas DataFrame
        DataFrame of predictions, with similar structure as df_measure
    """
    # mode = 'confirmed'
    mode = 'active'
    df_measure_confirmed = df_measure[mode]
    colors = px.colors.qualitative.Dark24
    n_colors = len(colors)
    fig = go.Figure()
    hovertemplate_measure = '<b>%{meta}</b><br>%{x}<br>%{y:.0f}<extra></extra>'
    hovertemplate_prediction = '<b>%{meta}<br>prediction</b><br>%{x}<br>%{y:.0f}<extra></extra>'
    for i, country in enumerate(df_measure_confirmed.columns):
        fig.add_trace(go.Scatter(x=df_measure_confirmed.index,
                                 y=df_measure_confirmed[country],
                                 name=country[1], mode='markers+lines',
                                 marker_symbol = SymbolValidator().values[i],
                                 marker_color=colors[i%n_colors],
                                 line_color=colors[i%n_colors],
                                 meta=country[1],
                                 hovertemplate=hovertemplate_measure,
                                 visible=False))
    prediction = df_prediction['prediction']
    upper_bound = df_prediction['upper_bound']
    lower_bound = df_prediction['lower_bound']
    for i, country in enumerate(prediction.columns):
        # Do not plot predictions for a country with less than 50 cases
        if df_measure_confirmed[country][-1] < 50:
            continue
        fig.add_trace(go.Scatter(x=prediction.index,
                                 y=prediction[country],
                                 name='+' + country[1], mode='lines',
                                 line_dash='dash',
                                 line_color=colors[i%n_colors],
                                 showlegend=False,
                                 meta=country[1],
                                 hovertemplate=hovertemplate_prediction,
                                 visible=False))
        fig.add_trace(go.Scatter(x=upper_bound.index,
                                 y=upper_bound[country],
                                 name='+' + country[1], mode='lines',
                                 line_dash='dot',
                                 line_color=colors[i%n_colors],
                                 showlegend=False,
                                 visible=False,
                                 hoverinfo='skip',
                                 line_width=.8))
        fig.add_trace(go.Scatter(x=lower_bound.index,
                                 y=lower_bound[country],
                                 name='+' + country[1], mode='lines',
                                 line_dash='dot',
                                 line_color=colors[i%n_colors],
                                 showlegend=False,
                                 visible=False,
                                 hoverinfo='skip',
                                 line_width=.8))

    last_day = df_measure_confirmed.index.max()
    day = pd.DateOffset(days=1)
    fig.update_layout(title='',
            xaxis=dict(rangeslider_visible=True,
                range=(last_day - 10 * day,
                       last_day + 4 * day)))
    fig.update_layout(
        showlegend=True,
        updatemenus=[
        dict(
            type = "buttons",
            direction = "left",
            buttons=list([
                dict(
                    args=[{"visible": [False,]*len(df_measure_confirmed.columns)}],
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
            pad={"r": 10, "t": 0, "b": 0},
            showactive=True,
            x=0.05,
            xanchor="left",
            y=1.05,
            yanchor="top",
            font_color='black',
        ),
        ],
        xaxis_tickfont_size=LABEL_FONT_SIZE - 4,
        yaxis_tickfont_size=LABEL_FONT_SIZE - 4,
        height=FIRST_LINE_HEIGHT,
        margin=dict(t=0, b=0.02),
        # The legend position + font size
        # See https://plot.ly/python/legend/#style-legend
        legend=dict(x=.05, y=.8, font_size=LABEL_FONT_SIZE,
                    title="Active cases in"),
)
    return fig


if __name__ == '__main__':
    from data_input import get_all_data, tidy_most_recent

    df, df_prediction = get_all_data()
    # most recent date, tidy format (one column for countries)
    df_tidy = tidy_most_recent(df)
    df_tidy_fatalities = tidy_most_recent(df, 'death')
    df_tidy_recovered = tidy_most_recent(df, 'recovered')

    fig1 = make_map(df_tidy, df_tidy_fatalities, df_tidy_recovered)
    fig2 = make_timeplot(df, df_prediction)
