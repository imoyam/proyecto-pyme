import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import os

st.set_page_config(
    page_title="Dashboard de Ventas de Café",
    layout="wide",
    initial_sidebar_state="expanded"
)

data = os.path.join("data", "Coffe_sales.xlsx")

@st.cache_data
def load_data():
    df = pd.read_excel(data)
    df["date"] = pd.to_datetime(df["date"])
    return df
df = load_data()

#sidebar
st.sidebar.header("Filtros")
fecha_input = st.sidebar.date_input(
    "Rango de fechas",
    value=(df["date"].min(), df["date"].max())
)
if isinstance(fecha_input, tuple) and len(fecha_input) == 2:
    fecha_min, fecha_max = fecha_input
else:
    fecha_min = fecha_max = fecha_input
bebidas = st.sidebar.multiselect(
    "Selecciona las bebidas",
    options=df["coffee_name"].unique(),
    default=df["coffee_name"].unique()
)
df_filtered = df[
    (df["date"] >= pd.to_datetime(fecha_min)) &
    (df["date"] <= pd.to_datetime(fecha_max)) &
    (df["coffee_name"].isin(bebidas))
]


#KPI 
st.title("Ventas de cafe dashboard")

col1,col2,col3,col4 = st.columns(4)
col1.metric("Total Ventas", f"${df_filtered['money'].sum():,.0f}")
col2.metric("Venta Promedio", f"${df_filtered['money'].mean():,.2f}")
col3.metric("Transacciones", f"{df_filtered.shape[0]:,.0f}")
col4.metric("Clientes Únicos", f"{df_filtered['card'].nunique():,.0f}")
st.markdown("---")
# nombres de las tabs
tab1,tab2,tab3,tab4 = st.tabs([
    "ventas durante el tiempo",
    "Ventas por bebida",
    "Ventas por hora del día",
    "Metodos de pago"
])

with tab2:
    top_bebidas = df_filtered.groupby("coffee_name")["money"].sum().sort_values(ascending=False).reset_index()
    fig_bebidas = px.bar(
        top_bebidas.head(10),
        x="money", y="coffee_name",
        orientation="h",
        title="Top 10 Bebidas Más Vendidas"
    )
    st.plotly_chart(fig_bebidas, use_container_width=True)
with tab3:
    col_a, col_b = st.columns(2)

    ventas_hora = df_filtered.groupby("hour_of_day")["money"].sum().reset_index()
    fig_hora = px.bar(
        ventas_hora, x="hour_of_day", y="money",
        title="Ventas por Hora del Día"
    )
    col_a.plotly_chart(fig_hora, use_container_width=True)

    ventas_dia = df_filtered.groupby("Weekday")["money"].sum().reset_index()
    fig_dia = px.bar(
        ventas_dia, x="Weekday", y="money",
        title="Ventas por Día de la Semana"
    )
    col_b.plotly_chart(fig_dia, use_container_width=True)

with tab4:
    ventas_pago = df_filtered.groupby("cash_type")["money"].sum().reset_index()
    fig_pago = px.pie(
        ventas_pago, names="cash_type", values="money",
        title="Distribución por Método de Pago"
    )
    st.plotly_chart(fig_pago, use_container_width=True)