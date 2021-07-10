import streamlit as st
import pandas as pd
import os, sys

# TESTING: python -m streamlit run D:\Documentos\TheBridge\bridge_datascience_JorgeGarcia\Text_Generation_Project\src\dashboard\app.py

root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root)

from src.utils.dashboard_tb import StreamFuncs

dfpath = root + os.sep + 'data' + os.sep + 'BASE.csv'
df = pd.read_csv(dfpath)

stream = StreamFuncs(df, root)

df = None
st.set_option('deprecation.showPyplotGlobalUse', False)
    
menu = st.sidebar.selectbox('Menu:',
            options=["Welcome", "Visualization", "JSON API-Flask", "Model Prediction", "Models From SQL Database", "Conclusions"])

if menu == 'Welcome':
    stream.greet()

if menu == 'Visualization':
    stream.barchart_page()

if menu == 'JSON API-Flask':
    stream.flask_page()

if menu == 'Model Prediction':
    pass

if menu == 'Models From SQL Database':
    pass

if menu == 'Conclusions':
    pass