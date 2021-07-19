import streamlit as st

menu = st.sidebar.selectbox('Menu:',
            options=["Bienvenida"])

if menu == 'Bienvenida':
    st.title("Hola clase, soy el título")
    st.write('Hola clase, soy la descripción')
    st.write('Os imagináis qué tenéis que hacer, ¿verdad?')
    st.write('Hacer lo mismo pero con vuestro proyecto :)')
