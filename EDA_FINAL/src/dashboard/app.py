import streamlit as st
import pandas as pd
import os, sys

# TESTING: python -m streamlit run D:\Documentos\TheBridge\bridge_datascience_JorgeGarcia\EDA_FINAL\src\dashboard\app.py

path = os.path.dirname(os.path.dirname(__file__))

sys.path.append(path)

from utils.dashboard_tb import StreamFuncs

data = pd.read_csv(os.path.dirname(path) + os.sep + 'data' + os.sep + 'MAIN_DATASET.csv')
expanse = pd.read_csv(os.path.dirname(path) + os.sep + 'data' + os.sep + 'GENRE_DATASET.csv')
word_stats = pd.read_csv(os.path.dirname(path) + os.sep + 'data' + os.sep + 'WORD_STATS.csv')

stream = StreamFuncs(data, expanse, word_stats)

df = None
st.set_option('deprecation.showPyplotGlobalUse', False)
    
menu = st.sidebar.selectbox('Menu:',
            options=["Greetings", "Genre Pie Chart", "Rating Distribution", "Rating Tendencies",
                "WordCloud", "Treemap", "Base Word Bar Chart", "Flask", "Conclusions"])

if menu == 'Greetings':
    st.title('Netflix Title Plot Popularity Detailed Analysis')
    stream.greet()

if menu == 'Genre Pie Chart':
    st.title('Netflix Title Plot Popularity Detailed Analysis')
    stream.piechart_page()

if menu == 'Rating Distribution':
    st.title('Netflix Title Plot Popularity Detailed Analysis')
    stream.distribution_page()

if menu == 'Rating Tendencies':
    st.title('Netflix Title Plot Popularity Detailed Analysis')
    stream.tendency_page()

if menu == 'WordCloud':
    st.title('Netflix Title Plot Popularity Detailed Analysis')
    stream.cloud_page(path)

if menu == 'Treemap':
    st.title('Netflix Title Plot Popularity Detailed Analysis')
    stream.treemap_page()

if menu == 'Base Word Bar Chart':
    st.title('Netflix Title Plot Popularity Detailed Analysis')
    stream.barchart_page()

if menu == 'Flask':
    st.title('Netflix Title Plot Popularity Detailed Analysis')
    stream.flask_page()

if menu == 'Conclusions':
    st.title('Netflix Title Plot Popularity Detailed Analysis')
    stream.conclude()

if __name__ == '__main__':
    print(path)