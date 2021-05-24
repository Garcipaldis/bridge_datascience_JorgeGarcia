import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
from utils import data_path

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets = external_stylesheets)

df = pd.read_csv(data_path)

fig = px.histogram(df, x="Rating", range_x=[0.8, 5.2])

app.layout = html.Div(children=[
    html.H1('Dashboard aplicaciones Android'),
    html.Div(children='''
    Primera app de aprendizaje con Dash
    '''),
    dcc.Graph(
        id='example-graph',
        figure=fig
    )
])


if __name__ == '__main__':
    app.run_server(host="0.0.0.0", port=1010, debug=True)