import dash
import dash_html_components as html
import dash_core_components as dcc
from make_functions import make_map, make_timeplot
from data_input import get_data

from pycovid import pycovid
df_all = pycovid.getCovidCases()
df_all['iso'] = df_all['alpha-3']
df_all = df_all.sort_values(by='date')
# Sum data for provinces
group_columns = list(df_all.columns)
group_columns.remove('cases')
group_columns.remove('province_state')
df = df_all.groupby(group_columns).sum()
df_all = df.reset_index()


fig1 = make_map(df_all)
fig2 = make_timeplot(get_data())

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

