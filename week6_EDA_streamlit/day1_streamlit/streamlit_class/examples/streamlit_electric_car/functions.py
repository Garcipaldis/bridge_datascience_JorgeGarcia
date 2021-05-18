import streamlit as st
from PIL import Image
import pandas as pd
import os 
path = os.path.dirname(__file__)

def configuracion():
    st.set_page_config(page_title='Cargatron', page_icon=':electric_plug:', layout="wide")

def menu_home(df):

    st.header("Puntos de carga para coches electricos en Madrid.")
    img = Image.open(path + os.sep + 'puntos-recarga-madrid.jpg')
    st.image(img, use_column_width='auto')

    with st.beta_expander("De que me hablas?"):
        st.write("""
        Ante el problema climatico al que nos
        enfrentamos el coche electrico se plantea
        como una solución posible. Aquí queremos
        facilitarte que encuentres tu puesto de 
        carga más cercano.""")

    with st.echo():
        st.write("Esta forma tienen nuestros datos")
        st.dataframe(df)


@st.cache(suppress_st_warning=True)
def cargar_datos(csv_path, uploaded_file):

    if (uploaded_file is not None):
        #uploaded_file.seek(0)
        df = pd.read_csv(uploaded_file)
        st.write("Hemos leido el csv")

    else:
        df = pd.read_csv(csv_path, sep=';')
        df = df.rename(columns={'latidtud': 'lat', 'longitud': 'lon'})

    st.balloons()

    return df

def menu_datos(df):
    st.subheader('Mapa:')
    dibujar_mapa(df)
    cargadores_por_distrito = df.groupby('DISTRITO')['Nº CARGADORES'].sum()
    st.subheader('Cargadores por distrito:')
    st.bar_chart(cargadores_por_distrito)

    cargadores_por_operador = df.groupby('OPERADOR')['Nº CARGADORES'].sum()
    st.subheader('Cargadores por Operador:')
    st.bar_chart(cargadores_por_operador)


def dibujar_mapa(df, zoom=11):
    st.map(df, zoom=zoom)


def menu_filtrado(df):

    st.sidebar.subheader("Filtros:")

    distritos, filtro_distrito, tamano, filtro_tamano, operador, filtro_operador = opciones_filtros(df)

    df_filtrado = filtrar(df, distritos, filtro_distrito, tamano, filtro_tamano, operador, filtro_operador)

    if df_filtrado.shape[0] == 0:
        st.warning("Los filtros que has seleccionado no nos devuelven ningun punto de carga")
        st.stop()

    graficas(df_filtrado, filtro_distrito, filtro_operador)

def opciones_filtros(df):
    distritos = st.sidebar.selectbox(
        'Selecciona el distrito que te interese:',
        options=df.DISTRITO.unique().tolist())
    filtro_distrito = st.sidebar.checkbox('Quiero filtrar por distrito')

    tamano = st.sidebar.select_slider("Selecciona el numero de cargadores por puesto",
                                      options=range(min(df.iloc[:, 3]), max(df.iloc[:, 3]) + 1),
                                      value=(min(df.iloc[:, 3]), max(df.iloc[:, 3])))
    filtro_tamano = st.sidebar.checkbox('Quiero filtrar por tamaño')

    operador = st.sidebar.selectbox(
        'Selecciona el operador que te interese:',
        options=df.OPERADOR.unique().tolist())
    filtro_operador = st.sidebar.checkbox('Quiero filtrar por operador')

    return distritos, filtro_distrito, tamano, filtro_tamano, operador, filtro_operador

def filtrar(df, distritos, filtro_distrito, tamano, filtro_tamano, operador, filtro_operador):

    if filtro_distrito:
        df = df.loc[df['DISTRITO'] == distritos, :]

    if filtro_tamano:
        df = df.loc[(df['Nº CARGADORES'] >= tamano[0]) & (df['Nº CARGADORES'] <= tamano[1]), :]

    if filtro_operador:
        df = df.loc[df['OPERADOR'] == operador, :]

    return df

def graficas(df_filtrado, filtro_distrito, filtro_operador):
    col1, col2 = st.beta_columns([3, 2])

    with col1:
        st.subheader('Mapa:')
        zoom = 11
        if filtro_distrito:
            zoom = 13

        dibujar_mapa(df_filtrado, zoom)

    with col2:
        if not filtro_distrito:
            cargadores_por_distrito = df_filtrado.groupby('DISTRITO')['Nº CARGADORES'].sum()
            st.subheader('Cargadores por distrito:')
            st.bar_chart(cargadores_por_distrito)

        if not filtro_operador:
            cargadores_por_operador = df_filtrado.groupby('OPERADOR')['Nº CARGADORES'].sum()
            st.subheader('Cargadores por Operador:')
            st.bar_chart(cargadores_por_operador)

        cargadores_por_tamano = df_filtrado['Nº CARGADORES'].value_counts()
        st.subheader('Cargadores por distrito:')
        st.bar_chart(cargadores_por_tamano)
