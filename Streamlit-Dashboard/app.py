import streamlit as st
import pandas as pd
import plotly.express as px

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Coffee Shop Sales Analysis", layout="wide")

# Estilo personalizado para el sidebar y colores (opcional)
st.markdown("""
    <style>
    [data-testid="stSidebar"] { background-color: #3d2b1f; }
    .stMetric { background-color: #fdf5e6; padding: 15px; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- CARGA DE DATOS ---
@st.cache_data
def load_data():
    df = pd.read_csv("../Data/coffee_shop_sales.csv")
    
    # Opción A: Si sabes que el día siempre va primero
    df['transaction_date'] = pd.to_datetime(df['transaction_date'], dayfirst=True)
    
    # Opción B (Más segura si hay formatos mezclados):
    # df['transaction_date'] = pd.to_datetime(df['transaction_date'], format='mixed', dayfirst=True)
    
    df['Month_Name'] = df['transaction_date'].dt.month_name()
    # Aprovechamos para crear la columna 'Day' para la página 2
    df['Day'] = df['transaction_date'].dt.day 
    return df

df = load_data()

# --- SIDEBAR / FILTROS ---
st.sidebar.title("☕ Coffee Analytics")
st.sidebar.markdown("---")

# Opción "Todas" para el filtro de mes
meses_disponibles = ["Todas"] + list(df['Month_Name'].unique())
mes_seleccionado = st.sidebar.selectbox("Filtrar por Mes:", meses_disponibles)

tiendas_disponibles = ["Todas"] + list(df['store_location'].unique())
tienda_seleccionada = st.sidebar.selectbox("Filtrar por Tienda:", tiendas_disponibles)

# --- LÓGICA DE FILTRADO DINÁMICO ---
df_filtered = df.copy()

if mes_seleccionado != "Todas":
    df_filtered = df_filtered[df_filtered['Month_Name'] == mes_seleccionado]

if tienda_seleccionada != "Todas":
    df_filtered = df_filtered[df_filtered['store_location'] == tienda_seleccionada]

# --- VISTA GENERAL (OVERVIEW) ---
st.title("📊 Overview: Rendimiento Global")
st.markdown(f"Mostrando datos de: **{mes_seleccionado}** | Tienda: **{tienda_seleccionada}**")

# Fila 1: KPIs Globales
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Ventas Totales", f"${df_filtered['Total_Bill'].sum():,.2f}")
with col2:
    st.metric("Volumen de Productos", f"{df_filtered['transaction_qty'].sum():,}")
with col3:
    st.metric("Total Tickets", f"{df_filtered['transaction_id'].nunique():,}")

st.markdown("---")

# Fila 2: Visualizaciones de Distribución
c1, c2 = st.columns([6, 4]) # 60% y 40% de ancho

with c1:
    st.subheader("Ventas por Categoría de Producto")
    # Gráfico de barras horizontales como en tu imagen
    fig_cat = px.bar(
        df_filtered.groupby('product_category')['Total_Bill'].sum().sort_values(ascending=True).reset_index(),
        x='Total_Bill', y='product_category', orientation='h',
        color_discrete_sequence=['#6f4e37'],
        template="simple_white"
    )
    st.plotly_chart(fig_cat, use_container_width=True)

with c2:
    st.subheader("% Ventas por Tienda")
    fig_pie = px.pie(
        df_filtered, values='Total_Bill', names='store_location',
        hole=0.5,
        color_discrete_sequence=['#3d2b1f', '#6f4e37', '#c3a689']
    )
    st.plotly_chart(fig_pie, use_container_width=True)

# Fila 3: Tabla de Resumen Global (La que tienes abajo a la derecha en la Imagen 0)
st.subheader("Resumen Ejecutivo de Categorías")
resumen = df_filtered.groupby('product_category').agg({
    'Total_Bill': 'sum',
    'unit_price': 'mean',
    'transaction_qty': 'sum'
}).reset_index()

# Calculamos el % del total para la tabla
total_v = resumen['Total_Bill'].sum()
resumen['% sales'] = (resumen['Total_Bill'] / total_v) * 100

st.dataframe(
    resumen.style.format({
        'Total_Bill': '${:,.2f}',
        'unit_price': '${:,.2f}',
        '% sales': '{:.2f}%',
        'transaction_qty': '{:,}'
    }), 
    use_container_width=True
)