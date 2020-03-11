import dash
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
    ])


if __name__ == '__main__':
    app.run_server(debug=True)

