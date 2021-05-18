import streamlit as st
import functions as ft
import os

    
path = os.path.dirname(__file__)


csv_path = path + os.sep + 'red_recarga_acceso_publico _2021.csv'

ft.configuracion()

slider_csv = st.sidebar.file_uploader("¿Tienes unos datos mejores?", type=['csv'])
df = ft.cargar_datos(csv_path, slider_csv)

menu = st.sidebar.selectbox('Menu:',
                            options=['home','datos','filtrado'])

st.title("Cargatron")

if menu == 'home':
    ft.menu_home(df)
elif menu == 'datos':
    ft.menu_datos(df)
elif menu == 'filtrado':
    ft.menu_filtrado(df)
