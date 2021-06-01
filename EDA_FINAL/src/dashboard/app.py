import streamlit as st
import pandas as pd
import os, sys

# TESTING: python -m streamlit run D:\Documentos\TheBridge\bridge_datascience_JorgeGarcia\EDA_FINAL\src\dashboard\app.py

path = os.path.dirname(os.path.dirname(__file__))

sys.path.append(path)

from utils.dashboard_tb import StreamFuncs

data = pd.read_csv(os.path.dirname(path) + os.sep + 'data' + os.sep + 'BASE.csv')
expanse = pd.read_csv(os.path.dirname(path) + os.sep + 'data' + os.sep + 'EXPANSE.csv')
word_stats = pd.read_csv(os.path.dirname(path) + os.sep + 'data' + os.sep + 'WORD_STATS.csv')

stream = StreamFuncs(data, expanse, word_stats)

df = None
st.set_option('deprecation.showPyplotGlobalUse', False)
    
menu = st.sidebar.selectbox('Menu:',
            options=["Greetings", "Datasets", "Genre Pie Chart", "Rating Distribution", "Rating Tendencies",
                "WordCloud", "Treemap", "Base Word Bar Chart", "Flask", "Conclusions"])

if menu == 'Greetings':
    stream.greet()

if menu == 'Datasets':
    stream.dataset_page()

if menu == 'Genre Pie Chart':
    stream.piechart_page()

if menu == 'Rating Distribution':
    stream.distribution_page()

if menu == 'Rating Tendencies':
    stream.tendency_page()

if menu == 'WordCloud':
    stream.cloud_page(path)

if menu == 'Treemap':
    stream.treemap_page()

if menu == 'Base Word Bar Chart':
    stream.barchart_page()

if menu == 'Flask':
    stream.flask_page()

if menu == 'Conclusions':
    stream.conclude()
