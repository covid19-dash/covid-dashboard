"""
Utility functions to generate plotly figures from dataframe. Called in app.py
"""

import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import pandas as pd
import plotly.io as pio
from plotly.validators.scatter.marker import SymbolValidator

from data_input import normalize_by_population, normalize_by_population_wide

pio.templates.default = "plotly_white"

FIRST_LINE_HEIGHT = 600

LABEL_FONT_SIZE = 20


def make_map(df, df_fatalities):
    """
    Build figure with map of total number of cases

    Parameters
    ----------
    df: pandas DataFrame
        Tidt dataframe of confirmed cases
    df_fatalities: pandas DataFrame
        Tidy dataframe of fatalities
    """
    normalized_values = normalize_by_population(df)
    # Plot per Million individual
    normalized_values *= 1e6
    hovertemplate = ('<b>Country</b>:%{customdata[0]}<br>' +
                     '<b>Confirmed cases per million</b>: %{customdata[1]:.1f}<br>' +
                     '<b>Confirmed cases</b>: %{customdata[2]}<br>' +
                     '<b>Fatalities</b>: %{customdata[3]}'
                     )
    fig = px.choropleth(df, locations='iso',
                    color=np.log10(normalized_values),
                    custom_data=[df['country_region'], normalized_values,
                                 df['value'], df_fatalities['value'],
                                 ],
                    color_continuous_scale='Plasma_r',
                    labels={'color': 'Confirmed<br>cases<br>per<br>Million'})
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


def make_timeplot(df_measure, df_prediction, countries=None):
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

    countries: list or None (default)
        list of countries to use for the figure. If None, all countries are used.
    """
    # active cases
    mode = 'confirmed'
    df_measure_confirmed = df_measure[mode]
    df_measure_confirmed = normalize_by_population_wide(df_measure_confirmed)
    # Plot per million
    df_measure_confirmed *= 1e6
    colors = px.colors.qualitative.Dark24
    n_colors = len(colors)
    fig = go.Figure()
    hovertemplate_measure = '<b>%{meta}</b><br>%{x}<br>%{y:.0f} per Million<extra></extra>'
    hovertemplate_prediction = '<b>%{meta}<br>prediction</b><br>%{x}<br>%{y:.0f} per Million<extra></extra>'
    for i, country in enumerate(df_measure_confirmed.columns):
        if countries and country[1] not in countries:
            continue
        fig.add_trace(go.Scatter(x=df_measure_confirmed.index,
                                 y=df_measure_confirmed[country],
                                 name=country[1], mode='markers+lines',
                                 marker_symbol = SymbolValidator().values[i],
                                 marker_color=colors[i%n_colors],
                                 line_color=colors[i%n_colors],
                                 meta=country[1],
                                 hovertemplate=hovertemplate_measure,
                                 visible=True))

    # predictions
    prediction = df_prediction['prediction']
    upper_bound = df_prediction['upper_bound']
    lower_bound = df_prediction['lower_bound']
    prediction = normalize_by_population_wide(prediction)
    prediction *= 1e6
    upper_bound = normalize_by_population_wide(upper_bound)
    upper_bound *= 1e6
    lower_bound = normalize_by_population_wide(lower_bound)
    lower_bound *= 1e6
    for i, country in enumerate(prediction.columns):
        if countries and country[1] not in countries:
            continue
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
                                 visible=True))
        fig.add_trace(go.Scatter(x=upper_bound.index,
                                 y=upper_bound[country],
                                 name='+' + country[1], mode='lines',
                                 line_dash='dot',
                                 line_color=colors[i%n_colors],
                                 showlegend=False,
                                 visible=True,
                                 hoverinfo='skip',
                                 line_width=.8))
        fig.add_trace(go.Scatter(x=lower_bound.index,
                                 y=lower_bound[country],
                                 name='+' + country[1], mode='lines',
                                 line_dash='dot',
                                 line_color=colors[i%n_colors],
                                 showlegend=False,
                                 visible=True,
                                 hoverinfo='skip',
                                 line_width=.8))
    # fatalities
    mode = 'death'
    df_measure_death = df_measure[mode]
    df_measure_death = normalize_by_population_wide(df_measure_death)
    # Plot per million
    df_measure_death *= 1e6
    colors = px.colors.qualitative.Dark24
    n_colors = len(colors)
    hovertemplate_fatalities = '<b>%{meta}<br>fatalities</b><br>%{x}<br>%{y:.0f} per Million<extra></extra>'
    for i, country in enumerate(df_measure_death.columns):
        if countries and country[1] not in countries:
            continue
        fig.add_trace(go.Scatter(x=df_measure_death.index,
                                 y=df_measure_death[country],
                                 name='  ' + country[1], mode='markers+lines',
                                 marker_symbol = SymbolValidator().values[i],
                                 marker_color=colors[i%n_colors],
                                 line_color=colors[i%n_colors],
                                 meta=country[1],
                                 hovertemplate=hovertemplate_fatalities,
                                 visible=True))

    last_day = df_measure_confirmed.index.max()
    day = pd.DateOffset(days=1)
    fig.update_layout(title='',
            xaxis=dict(rangeslider_visible=True,
                range=(last_day - 10 * day,
                       last_day + 4 * day)))


    # # vertical line to separate the last day of measurements from prediction
    fig.add_shape(
        # Line Vertical
        dict(
            type='line',
            xref='x',
            yref='paper',
            x0=last_day,
            y0=0.05,
            x1=last_day,
            y1=0.95,
            line=dict(
                color="gray",
                dash='dash',
                width=1
            )
    ))


    fatalities_annotation = dict(x=0.1,
                                 y=0.95,
                                 xref='paper',
                                 yref='paper',
                                 showarrow=False,
                                 font_size=LABEL_FONT_SIZE,
                                 text='Fatalities per Million',
                                 visible=False,
                                 )
    confirmed_annotation = dict(x=0.1,
                                 y=0.95,
                                 xref='paper',
                                 yref='paper',
                                 showarrow=False,
                                 font_size=LABEL_FONT_SIZE,
                                 text='Confirmed cases per Million',
                                 visible=True,
                                 )
    drag_handle_annotation = dict(x=1,
                                   y=-0.1,
                                   xref='paper',
                                   yref='paper',
                                   showarrow=False,
                                   font_size=LABEL_FONT_SIZE - 6,
                                   font_color="DarkSlateGray",
                                   text="Drag handles below to change time window",
                                   align="right")


    fig.update_layout(
        showlegend=True,
        annotations=[fatalities_annotation,
                     confirmed_annotation,
                     drag_handle_annotation],
        xaxis_tickfont_size=LABEL_FONT_SIZE - 4,
        yaxis_tickfont_size=LABEL_FONT_SIZE - 4,
        yaxis_type='linear',
        height=FIRST_LINE_HEIGHT,
        margin=dict(t=0, b=0.02),
        # The legend position + font size
        # See https://plot.ly/python/legend/#style-legend
        legend=dict(x=.05, y=.8, font_size=LABEL_FONT_SIZE)
    )



    return fig


if __name__ == '__main__':
    from data_input import get_all_data, tidy_most_recent

    df, df_prediction = get_all_data()
    # most recent date, tidy format (one column for countries)
    df_tidy = tidy_most_recent(df)
    df_tidy_fatalities = tidy_most_recent(df, 'death')

    fig1 = make_map(df_tidy, df_tidy_fatalities)
    fig2 = make_timeplot(df, df_prediction)
