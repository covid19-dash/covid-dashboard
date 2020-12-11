"""
Dash app entry point

To launch the app, run

> python app.py

Dash documentation: https://dash.plot.ly/
"""
import os
import numpy as np

import dash
from dash.dependencies import Input, Output, State, ClientsideFunction
import dash_table
import dash_html_components as html
import dash_core_components as dcc

from make_figures import make_map, make_timeplot, FIRST_LINE_HEIGHT
from data_input import tidy_most_recent, get_all_data

if 'DEBUG' in os.environ:
    debug = os.environ['DEBUG'] == 'True'
    print(f"DEBUG environment variable present, DEBUG set to {debug}")
else:
    print("No DEBUG environment variable: defaulting to debug mode")
    debug = True

# -------- Data --------------------------
df, df_prediction = get_all_data()
# most recent date, tidy format (one column for countries)
df_tidy = tidy_most_recent(df)
df_tidy_fatalities = tidy_most_recent(df, 'death')
# keep only two columns for Dash DataTable
df_tidy_table = df_tidy[['country_region', 'value']]

df_tidy_table = df_tidy_table.reset_index()
# The indices initially displayed
initial_indices = list(df_tidy_table['value'].nlargest(3).index)
# We hardcode the second and third index shown as being China, and Korea
# to give a message of hope
# Not China so far, as it is still the top on in terms of numbers of
# total confirmed cases
#initial_indices[-1]  = np.where(df_tidy['iso'] == 'CHN')[0][0]
initial_indices[-2]  = np.where(df_tidy['iso'] == 'KOR')[0][0]

# ----------- Figures ---------------------
fig1 = make_map(df_tidy, df_tidy_fatalities)
fig2 = make_timeplot(df, df_prediction, countries=['France', 'Italy', 'Spain'])
fig_store = make_timeplot(df, df_prediction)

# ------------ Markdown text ---------------
# maybe later we can break the text in several parts
with open("text_block.md", "r") as f:
    intro_md = f.read()


# -----------App definition-----------------------
app = dash.Dash(__name__,
    external_stylesheets = [
        {
            'href': 'https://unpkg.com/purecss@1.0.1/build/pure-min.css',
            'rel': 'stylesheet',
            'integrity': 'sha384-oAOxQR6DkCoMliIh8yFnu25d7Eq/PHS21PClpwjOTeU2jRSq11vu66rf90/cZr47',
            'crossorigin': 'anonymous'
        },
        'https://unpkg.com/purecss@1.0.1/build/grids-responsive-min.css',
        'https://unpkg.com/purecss@1.0.1/build/base-min.css',
    ],
)
app.title = 'Covid-19: confirmed cases and extrapolation'
server = app.server

app.layout = html.Div([
    html.H1(children=app.title, className="title"),
    html.Div([#row
        html.Div([
            dcc.Graph(
                id='map', figure=fig1,
                config={
                    'displayModeBar': True,
                    'modeBarButtonsToRemove': ['toImage', 'lasso2d',
                                               'toggleSpikelines',
                                               'hoverClosestGeo']})
            ],
            className="pure-u-1 pure-u-lg-1 pure-u-xl-12-24",
            ),
        html.Div([
            dcc.RadioItems(id='radio-cases',
                options=[
                    {'label':'Confirmed cases', 'value': 'active'},
                    {'label': 'Fatalities', 'value': 'death'},
                ],
                value='active',
                labelStyle={'display': 'inline-block',
                            'padding-right': '0.5em'}
          ),
            dcc.RadioItems(id='log-lin',
                options=[
                    {'label':'log', 'value': 'log'},
                    {'label': 'linear', 'value': 'linear'},
                ],
                value='linear',
                labelStyle={'display': 'inline-block',
                            'padding-right': '0.5em'}
          ),

            dcc.Graph(
                id='plot', figure=fig2,
                config={
                    'displayModeBar': True,
                    'modeBarButtonsToRemove': ['toImage', 'zoom2d',
                                               'select2d', 'lasso2d',
                                               'toggleSpikelines',
                                               'resetScale2d']}
                )
            ],
            className="pure-u-1 pure-u-lg-1-2 pure-u-xl-8-24",
            ),
        dcc.Store(id='store', data=[fig_store, initial_indices]),
        html.Div([
            dash_table.DataTable(
                id='table',
                columns=[{"name": "Country", "id": "country_region"},
                         {"name": "Cases", "id": "value"},
                        ],
                data=df_tidy_table.to_dict('records'),
                filter_action="native",
                sort_action="native",
                sort_by=[{'column_id':'value', 'direction':'desc'}],
                row_selectable="multi",
                style_table={
                    'maxHeight': '{0}px'.format(FIRST_LINE_HEIGHT),
                    'overflowY': 'scroll'
                    },
                style_cell={
                    'height': 'auto', 'minHeight': '30px',
                    'minWidth': '0px', 'maxWidth': '10px',
                    'whiteSpace': 'normal'
                },
                style_filter={'height':'20px',
                    },
                style_cell_conditional=[
                    {'if': {'column_id': 'country_region'},
                     'width': '60%'},
                    {'if': {'column_id': 'value'},
                     'width': '40%'},
                ],
                style_data_conditional=[
                {
                    'if': {'row_index': 'odd'},
                    'backgroundColor': 'rgb(248, 248, 248)'
                }
                ],
            ),
            ],
            className="pure-u-1 pure-u-lg-1-2 pure-u-xl-4-24"),
        html.Div([html.Div([dcc.Markdown(intro_md,
                                         dangerously_allow_html=True)],
                  className="text-block")],
            className="pure-u-1 pure-u-lg-1 pure-u-xl-22-24"),
        html.Div([
            html.Div(['Latest data point: ',
                       df_tidy['date'].max().date()],
                     className="date")
            ],
            className="pure-u-1 pure-u-xl-1-24"),
        ],
        className="pure-g"),
        html.Div([
            html.Span('Contributors', className='contributors'),
            html.Ul([
                html.Li(['Gaël Varoquaux, Inria & McGill University']),
                html.Li(['Emmanuelle Gouillart, Plotly Inc']),
                html.Li(['Russell Poldrack, Stanford University']),
                html.Li(['Guillaume Lemaitre, Inria']),
                html.Li(['Ashwin Nalwade, NYU Courant']),
            ]),
            ],
            className="footer"),
        ],
    )

# ---------------------- Callbacks ---------------------------------
# Callbacks are all client-side (https://dash.plot.ly/performance)
# in order to transform the app into static html pages
# javascript functions are defined in assets/callbacks.js

app.clientside_callback(
    ClientsideFunction(
        namespace='clientside3',
        function_name='update_table'
    ),
    output=Output('table', 'selected_rows'),
    inputs=[
        Input('map', 'clickData'),
        Input('map', 'selectedData'),
        Input('table', 'data')
        ],
    state=[State('table', 'selected_rows'),
           State('store', 'data')],
    )


app.clientside_callback(
    ClientsideFunction(
        namespace='clientside',
        function_name='update_store_data'
    ),
    output=Output('plot', 'figure'),
    inputs=[
        Input('table', "data"),
        Input('table', "selected_rows"),
        Input('radio-cases', 'value'),
        Input('log-lin', 'value')],
    state=[State('store', 'data')],
    )



if __name__ == '__main__':
    app.run_server(debug=debug)
