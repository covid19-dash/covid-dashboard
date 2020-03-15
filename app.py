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
from make_figures import make_map, make_timeplot
from data_input import tidy_most_recent, get_all_data

if 'DEBUG' in os.environ:
    print("variable defined")
    debug = os.environ['DEBUG'] == 'True'
else:
    debug = True

# -------- Data --------------------------
df, df_prediction = get_all_data()
df_tidy = tidy_most_recent(df) # most recent date, tidy format (one column for countries)
df_tidy_table = df_tidy[['country_region', 'value']] # keep only two columns for Dash DataTable

# ----------- Figures ---------------------
fig1 = make_map(df_tidy)
fig2 = make_timeplot(df, df_prediction)

# ------------ Markdown text ---------------
# maybe later we can break the text in several parts
with open("text_block.md", "r") as f:
    intro_md = f.read()

# app definition
app = dash.Dash(__name__,
    external_stylesheets = [
        {
            'href': 'https://unpkg.com/purecss@1.0.1/build/pure-min.css',
            'rel': 'stylesheet',
            'integrity': 'sha384-oAOxQR6DkCoMliIh8yFnu25d7Eq/PHS21PClpwjOTeU2jRSq11vu66rf90/cZr47',
            'crossorigin': 'anonymous'
        },
        'https://unpkg.com/purecss@1.0.1/build/grids-responsive-min.css',
    ],
)
app.title = 'Covid-19: active cases and extrapolation'
server = app.server

app.layout = html.Div([
    html.Div([#row
        html.Div([
            dcc.Graph(id='map', figure=fig1)
            ],
            className="pure-u-1 pure-u-md-3-5",
            ),
        html.Div([
            dcc.Graph(id='plot', figure=fig2)
            ],
            className="pure-u-1 pure-u-md-2-5",
            ),
        dcc.Store(id='store', data=fig2),
        ],
        className="pure-g"),
    html.Div([#row
        html.Div([dcc.Markdown(intro_md)], className="eight columns"),
        html.Div([
            dash_table.DataTable(
                id='table',
                columns=[{"name": i, "id": i} for i in df_tidy_table],
                data=df_tidy_table.to_dict('records'),
                filter_action="native",
                sort_action="native",
                row_selectable="multi",
                style_table={
                    'maxHeight': '300px',
                    'overflowY': 'scroll'
                    },
            ),
            ], className="four columns")
        ], className="row"),
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
        Input('table', "derived_virtual_data"),
        Input('table', "derived_virtual_selected_rows")],
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
    state=[State('table', 'selected_rows')],
    )



if __name__ == '__main__':
    app.run_server(debug=debug)

