import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from PIL import Image
import os
import json
import requests

path = os.path.dirname(__file__)
df = None
    
menu = st.sidebar.selectbox('Menu:',
            options=["Greetings", "Base Visualization", "Word Stats", "Flask"])

if menu == 'Greetings':
    st.title('Welcome to my EDA Project')
    st.write('Netflix Title Plot Popularity Detailed Analysis')
    st.write('study made by: Jorge García Navarro')

if menu == 'Base Visualization':
    pass

if menu == 'Word Stats':
    pass

if menu == 'Flask':
    r = requests.get(url="http://localhost:6060/info?token_id=B53814652")
    response = r.json()
    df = pd.DataFrame(response)
    df = df.iloc[:, [4, 2, 5, 20, 23, 13]]
    st.table(df.head(20))
    droplist = st.sidebar.selectbox('Order by:',
                            options=['Netflix User Rating', 'IMDBb Rating', 'Year'])
    ascending = st.sidebar.checkbox('Ascending')
    if droplist == 'Netflix User Rating':
        if ascending:
            st.table(df.sort_values('netflix_rating').head(20))
        else:
            st.table(df.sort_values('netflix_rating', ascending=False).head(20))
    elif droplist == 'IMDBb Rating':
        if ascending:
            st.table(df.sort_values('imdbRating').head(20))
        else:
            st.table(df.sort_values('imdbRating', ascending=False).head(20))
    elif droplist == 'Year':
        if ascending:
            st.table(df.sort_values('Year').head(20))
        else:
            st.table(df.sort_values('Year', ascending=False).head(20))