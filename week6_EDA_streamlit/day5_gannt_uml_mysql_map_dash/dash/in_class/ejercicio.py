# visit http://localhost:6060/ in your web browser (or port and host that you use)

import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output
from utils import change_m, change_dollar, data_path

# --- style --- 
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
# --- app with style --- 
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.GRID, external_stylesheets])

df = pd.read_csv(data_path)
df["Price"] = df["Price"].apply(change_dollar)
df["Price"] = pd.to_numeric(df["Price"])
df["Reviews"] = df["Reviews"].apply(change_m)
df["Reviews"] = pd.to_numeric(df["Reviews"])

df = df[df['Reviews'] >= 1000000]

fig1 = px.scatter(df, x="Reviews", y="Rating", color='Category', hover_data=['App']) 
df_bars = df.groupby(['Category', 'Installs'])['App'].count().reset_index().sort_values('App', ascending=False)

fig2 = px.bar(df_bars, x="Category", y="App", color="Installs")

app.layout = html.Div(
        [
            dbc.Row(dbc.Col(html.H1(children='Dashboard aplicaciones Android'))),
            dbc.Row([
                    dbc.Col(dcc.Dropdown(
                        id='id_free_paid',
                        options=[
                            {'label': 'Free', 'value': 'Free'},
                            {'label': 'Paid', 'value': 'Paid'}
                        ],
                        value=['Free', 'Paid'],
                        multi=True
                    )),
                    dbc.Col(dcc.RangeSlider(
                        id='id_reviews_slider',
                        count=1,
                        min=df["Reviews"].min(),
                        max=df["Reviews"].max(),
                        step=1,
                        marks={
                                df["Reviews"].min(): {"label": str(df["Reviews"].min())},
                                df["Reviews"].max()//2: {"label":str(df["Reviews"].max()//2)},
                                df["Reviews"].max(): {"label":str(df["Reviews"].max())}
                            },
                        value=[df["Reviews"].min(), df["Reviews"].max()],
                        tooltip = { 'always_visible': True }
                    ))
            ]),

            dbc.Row([
                dbc.Col(
                        dcc.Graph(
                                id='scatter',
                                figure=fig1
                                )
                ),
                dbc.Col(
                        dcc.Graph(
                                id='bars',
                                figure=fig2
                                )
                )
            ])
        ]
)

@app.callback(Output('scatter', 'figure'),
              Output('bars', 'figure'),
              [Input('id_free_paid', 'value'),
              Input('id_reviews_slider', 'value')])
def update_graphs_selector(selected_type, reviews):
    filtered_df = df[df["Type"].isin(selected_type)]
    filtered_df = filtered_df[filtered_df["Reviews"] >= reviews[0]]
    filtered_df = filtered_df[filtered_df["Reviews"] <= reviews[1]]
    print("selected_type:", selected_type)
    print("reviews:", reviews)
    
    fig1 = px.scatter(filtered_df, x="Reviews", y="Rating", color='Category', hover_data=['App'])

    if selected_type:
        df_bars = filtered_df.groupby(['Category', 'Installs'])['App'].count().reset_index().sort_values('App', ascending=False)
        fig2 = px.bar(df_bars, x="Category", y="App", color="Installs")
    else:
        fig2 = px.bar(filtered_df, x="Category", y="App", color="Installs")

    fig1.update_layout()
    fig2.update_layout()
    return fig1, fig2

if __name__ == '__main__':
    app.run_server(host="0.0.0.0", port="6060", debug=True)