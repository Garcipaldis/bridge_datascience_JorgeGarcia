import streamlit as st
import pandas as pd
import os, sys

# TESTING: python -m streamlit run D:\Documentos\TheBridge\bridge_datascience_JorgeGarcia\Text_Generation_Project\src\dashboard\app.py

root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root)

from src.utils.dashboard_tb import StreamFuncs

dfpath = root + os.sep + 'data' + os.sep + 'BASE.csv'
df = pd.read_csv(dfpath)
settings_file = root + os.sep + 'src' + os.sep + "utils" + os.sep + "settings_sql.json"

stream = StreamFuncs(df, root, settings_file)

df = None
st.set_option('deprecation.showPyplotGlobalUse', False)
    
menu = st.sidebar.selectbox('Menu:',
            options=["Welcome", "Visualization", "JSON API-Flask", "Model Prediction", "Models From SQL Database"])

if menu == 'Welcome':
    stream.greet()

if menu == 'Visualization':
    stream.barchart_page()

if menu == 'JSON API-Flask':
    stream.flask_page()

if menu == 'Model Prediction':
    stream.model_page()

if menu == 'Models From SQL Database':
    stream.sql_page()