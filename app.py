import dash
from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_core_components as dcc
from make_functions import make_map, make_timeplot
from data_input import get_data, get_mapping

df = get_data()
mapping = get_mapping()

fig1 = make_map(df, mapping)
fig2 = make_timeplot(df)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
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
    ])


@app.callback(
    Output('plot', 'figure'),
    [Input('store', 'data')])
def update_store(data):
    return data


@app.callback(
    Output('store', 'data'),
    [Input('map', 'clickData'),
     Input('map', 'selectedData')],
    [State('store', 'data')])
def update_figure(clickData, selectedData, fig):
    if clickData is None and selectedData is None:
        return dash.no_update
    if clickData is not None:
        country = clickData['points'][0]['customdata'][1]
        for trace in fig['data']:
            if trace['name'] == country:
                trace['visible'] = True
    if selectedData is not None:
        countries = [point['customdata'][1]
                        for point in selectedData['points']]
        for trace in fig['data']:
            if trace['name'] in countries:
                trace['visible'] = True
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)

