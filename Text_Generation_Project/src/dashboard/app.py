import streamlit as st
import pandas as pd
import os, sys

# TESTING: python -m streamlit run D:\Documentos\TheBridge\bridge_datascience_JorgeGarcia\Text_Generation_Project\src\dashboard\app.py

path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.append(path)

from utils.dashboard_tb import StreamFuncs

data = pd.read_csv(os.path.dirname(path) + os.sep + 'data' + os.sep + 'BASE.csv')
expanse = pd.read_csv(os.path.dirname(path) + os.sep + 'data' + os.sep + 'EXPANSE.csv')
word_stats = pd.read_csv(os.path.dirname(path) + os.sep + 'data' + os.sep + 'WORD_STATS.csv')

stream = StreamFuncs(data, expanse, word_stats)

df = None
st.set_option('deprecation.showPyplotGlobalUse', False)
    
menu = st.sidebar.selectbox('Menu:',
            options=["Welcome", "Visualization", "JSON API-Flask", "Model Prediction", "Models From SQL Database", "Conclusions"])

if menu == 'Welcome':
    pass

if menu == 'Visualization':
    pass

if menu == 'JSON API-Flask':
    pass

if menu == 'Model Prediction':
    pass

if menu == 'Models From SQL Database':
    pass

if menu == 'Conclusions':
    pass