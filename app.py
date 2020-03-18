"""
Dash app entry point

To launch the app, run

> python app.py

Dash documentation: https://dash.plot.ly/
"""
import os
import dash
from dash.dependencies import Input, Output, State, ClientsideFunction
import dash_table
import dash_html_components as html
import dash_core_components as dcc
from make_figures import make_map, make_timeplot, FIRST_LINE_HEIGHT
from data_input import tidy_most_recent, get_all_data, get_populations

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
df_tidy_recovered = tidy_most_recent(df, 'recovered')
# keep only two columns for Dash DataTable
df_tidy_table = df_tidy[['country_region', 'value']]
# The population information
pop = get_populations()

df_tidy_table = df_tidy_table.reset_index()
initial_indices = list(df_tidy_table['value'].nlargest(2).index)

# ----------- Figures ---------------------
fig1 = make_map(df_tidy, df_tidy_fatalities, df_tidy_recovered, pop)
fig2 = make_timeplot(df, df_prediction)

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
app.title = 'Covid-19: active cases and extrapolation'
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
        dcc.Store(id='store', data=[fig2, initial_indices]),
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
                     'width': '70%'},
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
        html.Div([html.Div([dcc.Markdown(intro_md)],
                  className="text-block")],
            className="pure-u-1 pure-u-lg-1 pure-u-xl-22-24"),
        ],
        className="pure-g"),
    ],
    )

# ---------------------- Callbacks ---------------------------------
# Callbacks are all client-side (https://dash.plot.ly/performance)
# in order to transform the app into static html pages
# javascript functions are defined in assets/callbacks.js

app.clientside_callback(
    ClientsideFunction(
        namespace='clientside2',
        function_name='get_store_data'
    ),
    output=Output('plot', 'figure'),
    inputs=[Input('store', 'data')])


app.clientside_callback(
    ClientsideFunction(
        namespace='clientside',
        function_name='update_store_data'
    ),
    output=Output('store', 'data'),
    inputs=[
        Input('table', "data"),
        Input('table', "selected_rows")],
    state=[State('store', 'data')],
    )


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



if __name__ == '__main__':
    app.run_server(debug=debug)
