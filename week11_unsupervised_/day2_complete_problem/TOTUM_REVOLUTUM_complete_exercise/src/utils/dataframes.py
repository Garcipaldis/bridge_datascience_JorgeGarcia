import streamlit as st
import pandas as pd 

def get_data_from_df(df):
    
    selected_values = df.iloc[:10,:].values
    
    return str(selected_values)

@st.cache(suppress_st_warning=True)
def load_csv_df(uploaded_file):
    df = None
    if uploaded_file != None:
        #uploaded_file.seek(0)
        df = pd.read_csv(uploaded_file, nrows=200)
        #st.write("csv Readed¡")
    st.balloons()
    return df

@st.cache(suppress_st_warning=True)
def load_csv_for_map(csv_path):
    if csv_path != None:
        df = pd.read_csv(csv_path, sep=';')
        df = df.rename(columns={'latidtud': 'lat', 'longitud': 'lon'})
    st.balloons()
    return df


