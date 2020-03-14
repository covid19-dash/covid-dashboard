"""
Dash app entry point

To launch the app, run

> python app.py

Dash documentation: https://dash.plot.ly/
"""

import dash
from dash.dependencies import Input, Output, State, ClientsideFunction
import dash_table
import dash_html_components as html
import dash_core_components as dcc
from make_figures import make_map, make_timeplot
from data_input import get_data, get_mapping, tidy_most_recent

# Data
df = get_data()
mapping = get_mapping()
df_tidy = tidy_most_recent(df)
df_tidy_table = df_tidy[['country_region', 'value']]

# Figures
fig1 = make_map(df_tidy, mapping)
fig2 = make_timeplot(df)

# Markdown text
with open("text_block.md", "r") as f:
    intro_md = f.read()


app = dash.Dash(__name__)
server = app.server 

app.layout = html.Div([
    html.Div([#row
        html.Div([
            dcc.Graph(id='map', figure=fig1)
            ],
            className="seven columns"
            ),
        html.Div([
            dcc.Graph(id='plot', figure=fig2)
            ],
            className="five columns"
            ),
        dcc.Store(id='store', data=fig2)
    ], className="row"),
    html.Div([#row
        html.Div([dcc.Markdown(intro_md)], className="six columns"),
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
            )
            ], className="six columns")
        ], className="row", style={'font-color':'white'}),
    ],
    )

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
        Input('map', 'clickData'),
            Input('map', 'selectedData')],
    state=[State('store', 'data')],
    )



if __name__ == '__main__':
    app.run_server()

