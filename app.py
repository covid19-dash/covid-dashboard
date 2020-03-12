import dash
from dash.dependencies import Input, Output, State, ClientsideFunction
import dash_html_components as html
import dash_core_components as dcc
from make_functions import make_map, make_timeplot
from data_input import get_data, get_mapping

df = get_data()
mapping = get_mapping()

fig1 = make_map(df, mapping)
fig2 = make_timeplot(df)


app = dash.Dash(__name__)
server = app.server 

app.layout = html.Div([
    html.Div([
        dcc.Graph(id='map', figure=fig1)
        ],
        className="six columns"
        ),
    html.Div([
        dcc.Graph(id='plot', figure=fig2)
        ],
        className="six columns"
        ),
    dcc.Store(id='store', data=fig2)
    ],
    style={'backgroundColor':'black'})

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
    app.run_server(debug=True)

