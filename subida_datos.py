import streamlit as st
import pandas as pd
import sqlite3

st.title("Envío de Datos de Ventas")

empresa = st.text_input("Nombre de tu empresa")
archivo = st.file_uploader("Sube tu archivo Excel o CSV", type=["csv", "xlsx"])

if archivo is not None and empresa:
    if archivo.name.endswith(".csv"):
        data = pd.read_csv(archivo)
    else:
        data = pd.read_excel(archivo)

    st.write("Vista previa de tus datos:")
    st.dataframe(data.head())

    if st.button("Enviar"):
        conn = sqlite3.connect("ventas.db")
        data["empresa"] = empresa
        data.to_sql("ventas", conn, if_exists="append", index=False)
        conn.close()
        st.success("Datos enviados correctamente.")
