from posixpath import dirname
import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from PIL import Image
import os, sys
import json
import requests

# TESTING: python -m streamlit run D:\Documentos\TheBridge\bridge_datascience_JorgeGarcia\EDA_FINAL\src\dashboard\app.py

path = os.path.dirname(os.path.dirname(__file__))

sys.path.append(path)

from utils.visualization_tb import Visualizer

data = pd.read_csv(os.path.dirname(path) + os.sep + 'data' + os.sep + 'MAIN_DATASET.csv')
expanse = pd.read_csv(os.path.dirname(path) + os.sep + 'data' + os.sep + 'GENRE_DATASET.csv')
word_stats = pd.read_csv(os.path.dirname(path) + os.sep + 'data' + os.sep + 'WORD_STATS.csv')

viz = Visualizer(data, expanse, word_stats)

df = None
st.set_option('deprecation.showPyplotGlobalUse', False)
    
menu = st.sidebar.selectbox('Menu:',
            options=["Greetings", "Genre Pie Chart", "Rating Distribution", "WordCloud", "Treemap", "Base Word Bar Chart", "Flask"])

if menu == 'Greetings':
    st.title('Welcome to my EDA Project')
    st.write('Netflix Title Plot Popularity Detailed Analysis')
    st.write('Study made by: Jorge García Navarro')
    st.pyplot(viz.generate_wordcloud('Romance', common=False))

if menu == 'Genre Pie Chart':
    top = st.sidebar.select_slider("Top Values",
                                    options=range(3, 21),
                                    value=10)
    st.pyplot(viz.plot_genre_pie(top))

if menu == 'Rating Distribution':
    droplist = st.sidebar.selectbox('Select Column Value:',
                            options=['netflix_rating', 'imdbRating'])
    kde = st.sidebar.checkbox('kde')
    st.pyplot(viz.plot_displot(x=droplist, kde=kde))

if menu == 'WordCloud':
    for genre in expanse.groupby('Genre').count().index:
        if len(expanse[expanse.Genre == genre]) > 10:
            st.text(genre)
            st.pyplot(viz.generate_wordcloud(genre, common=False))

if menu == 'Treemap':
    common = st.sidebar.checkbox('Use common words', value=True)
    st.plotly_chart(viz.plot_treemap(width=1000, height=600, common=common))

if menu == 'Base Word Bar Chart':
    droplist = st.sidebar.selectbox('Select Genre:',
                            options=list(expanse.groupby('Genre').count().index))
    top = st.sidebar.select_slider("Top Values",
                                    options=range(3, 21),
                                    value=10)
    common = st.sidebar.checkbox('Use common words', value=True)
    vertical = st.sidebar.checkbox('Vertical')
    if vertical:
        st.pyplot(viz.plot_word_barchart(droplist, x='word', y='%_occurrence',top=top, sort=1, show_values=True, common=common))
    else:
        st.pyplot(viz.plot_word_barchart(droplist, top=top, common=common))

if menu == 'Flask':
    r = requests.get(url="http://localhost:6060/info?token_id=B53814652")
    response = r.json()
    df = pd.DataFrame(response).dropna()
    df = df.iloc[:, [4, 2, 5, 20, 9, 13]]
    
    droplist = st.sidebar.selectbox('Order by:',
                            options=['Netflix User Rating', 'IMDBb Rating', 'Year'])
    ascending = st.sidebar.checkbox('Ascending')
    if droplist == 'Netflix User Rating':
        if ascending:
            df.sort_values('netflix_rating', inplace=True)
        else:
            df.sort_values('netflix_rating', inplace=True, ascending=False)
    elif droplist == 'IMDBb Rating':
        if ascending:
            df.sort_values('imdbRating', inplace=True)
        else:
            df.sort_values('imdbRating', inplace=True, ascending=False)
    elif droplist == 'Year':
        if ascending:
            df.sort_values('Year', inplace=True)
        else:
            df.sort_values('Year', inplace=True, ascending=False)
    st.dataframe(df)

if __name__ == '__main__':
    print(path)