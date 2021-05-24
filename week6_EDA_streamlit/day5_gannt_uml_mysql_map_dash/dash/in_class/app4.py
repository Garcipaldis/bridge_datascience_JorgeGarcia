# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
from utils import data_path

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.GRID, external_stylesheets])

df = pd.read_csv(data_path)

fig_blue = px.histogram(df, x="Rating", range_x=[0.8, 5.2], color_discrete_sequence=['blue'])
fig_red = px.histogram(df, x="Rating", range_x=[0.8, 5.2], color_discrete_sequence=['red'])
fig_orange = px.histogram(df, x="Rating", range_x=[0.8, 5.2], color_discrete_sequence=['orange'])
fig_black = px.histogram(df, x="Rating", range_x=[0.8, 5.2], color_discrete_sequence=['black'])
fig_green = px.histogram(df, x="Rating", range_x=[0.8, 5.2], color_discrete_sequence=['green'])

fig_box = px.box(df, x="Category", y="Rating", range_y=[0.8, 5.2])
fig_box2 = px.box(df, x="Category", y="Rating", color="Category", range_y=[0.8, 5.2])


app.layout = html.Div(
        [
            dbc.Row(dbc.Col(html.H1(children='Dashboard aplicaciones Android'))),
            dbc.Row(dbc.Col(html.Div(children='Primera app de aprendizaje con Dash'))),
            dbc.Row(
                [
                    dbc.Col(dcc.Graph(
                        id='graph-blue',
                        figure=fig_blue,
                        style={'height': '100%'}
                     )),

                    dbc.Col([
                            dbc.Row(dcc.Graph(
                                id='graph-box',
                                figure=fig_box
                            )),
                            dbc.Row(dcc.Graph(
                                id='graph-box2',
                                figure=fig_box2
                            ))]
                    )
                ]
            ),

            dbc.Row(
                [
                    dbc.Col(dcc.Graph(
                        id='graph-orange',
                        figure=fig_orange
                    )),
                    dbc.Col(dcc.Graph(
                        id='graph-black',
                        figure=fig_black
                    )),
                    dbc.Col(dcc.Graph(
                        id='graph-green',
                        figure=fig_green
                    ))
                ]
            )
        ]
)



if __name__ == '__main__':
    app.run_server(host="0.0.0.0", port=1010, debug=True)