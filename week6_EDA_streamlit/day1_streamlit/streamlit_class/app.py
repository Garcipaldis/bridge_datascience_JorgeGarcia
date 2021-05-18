# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from PIL import Image
import os
from utils.stream_config import create_sliders, draw_map
from utils.dataframes import get_data_from_df, load_csv_df, load_csv_for_map, load_normal_csv

path = os.path.dirname(__file__)
df = None
    
menu = st.sidebar.selectbox('Menu:',
            options=["Bienvenida", "Analizador", "Mapa con Globos"])

if menu == 'Bienvenida':
    st.title('¡Bienvenidos al Bootcamp de The Bridge!')
    st.write('Es un placer tenerte por aquí.')

if menu == 'Analizador':
    slider_csv = st.sidebar.file_uploader("Selecciona un CSV", type=['csv'])
    # Cargar el dataframe
    if type(slider_csv) != type(None): # Se cumple cuando subamos un archivo
        filtro_edades = st.sidebar.checkbox('Filtrar edades')
        df_slider = load_normal_csv(slider_csv)
        if filtro_edades:
            df_slider = df_slider[df_slider['age'] < 10 ]
        st.bar_chart(df_slider) # Muestra gráfico de barras de las columnas
        st.table(df_slider) # Muestra el dataframe

if menu == 'Mapa con Globos':
    csv_map_path = path + os.sep + "data" + os.sep + 'red_recarga_acceso_publico_2021.csv'
    df_map = load_csv_for_map(csv_map_path)
    draw_map(df_map)
    st.balloons()
        



if menu == 'Normal Dataframe':
    features = create_sliders()
    features_df  = pd.DataFrame([features])
    st.table(features_df)  
if menu == "Load Dataframe Columns": 
    st.write("https://raw.githubusercontent.com/plotly/datasets/master/2014_usa_states.csv")
    col1, col2 = st.beta_columns([2, 4])
    slider_csv = st.sidebar.file_uploader("Select CSV", type=['csv'])
    new_df_path = None
    df_slider = None
    df_writed = None
    with col1: 
        image = Image.open(path + os.sep + 'img' + os.sep + 'happy.jpg')
        st.image (image,use_column_width=True)
        #user_input = st.text_area("label goes here", "Escribe algo")
        new_df_path = st.text_input('CSV file path or url')
        if new_df_path:
            graph_slider_1 = None
            st.text(str(new_df_path))
            df_writed = pd.read_csv(str(new_df_path))
        if type(df_writed) != type(None):
            for i in range(5): st.write("")
            st.table(df_writed)
        if st.button('Show values'):
            values = None
            if type(df_writed) == type(pd.DataFrame()):
                values = get_data_from_df(df_writed)
            st.write(' Selected  '+ str(values))
        if type(slider_csv) != type(None):
            df_slider = load_csv_df(slider_csv)
            df_writed = None
        if type(df_slider) != type(None):
            for i in range(6): st.write("")
            st.table(df_slider) 
    with col2: 
        if type(df_slider) != type(None):
            df_slider["inds"] = df_slider["inds"].astype(float)
            df_slider["acidez"] = df_slider["acidez"].astype(float)
            graph_slider_1 = alt.Chart(df_slider).mark_circle().encode(
            x='inds', y='acidez', size="acidez", color="id")
            st.write(graph_slider_1)
        
        

if menu == "Graphs":
    slider_csv_graph = st.sidebar.file_uploader("Select CSV", type=['csv'])
    new_df_path_graph = None
    df_slider_graph = None
    df_slider_graph_copy = None
    hidden = None
    c_df_3 = None
    # show grahps

    if st.button('Show Graph'):
        df_3 = pd.DataFrame(
        np.random.randn(200, 3),
        columns=['a', 'b', 'c'])

        c_df_3 = alt.Chart(df_3).mark_circle().encode(
        x='a', y='b', size='c', color='c', tooltip=['a', 'b', 'c'])
        st.write(c_df_3)
    if type(slider_csv_graph) != type(None):
        columns = [None,]
        df_slider_graph = load_csv_df(slider_csv_graph)
        st.subheader('DF:')
        st.bar_chart(df_slider_graph)
        tamano = st.sidebar.select_slider("Number of values",
                                    options=range(0, df_slider_graph.shape[0]),
                                    value=100.0)
        columns.extend(list(df_slider_graph.columns))
    
        column_choose = st.sidebar.selectbox(
            'Select a column:',
            options=columns)
        if column_choose != None:
            st.bar_chart(df_slider_graph.head(tamano)[column_choose])

if menu == "Map":
    csv_map_path = path + os.sep + "data" + os.sep + 'red_recarga_acceso_publico_2021.csv'
    df_map = load_csv_for_map(csv_map_path)
    draw_map(df_map)