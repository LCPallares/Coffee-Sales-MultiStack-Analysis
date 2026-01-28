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

# Filtro de Mes (Equivalente a tus botones de arriba)
meses = ["January", "February", "March", "April", "May", "June"]
mes_seleccionado = st.sidebar.selectbox("Selecciona un Mes:", meses)

# Filtros adicionales
tienda = st.sidebar.multiselect("Tienda:", df['store_location'].unique(), default=df['store_location'].unique())

# Aplicar filtros al dataframe
df_filtered = df[(df['Month_Name'] == mes_seleccionado) & (df['store_location'].isin(tienda))]

# --- LÓGICA DE NEGOCIO (DAX -> PANDAS) ---
total_sales = df_filtered['Total_Bill'].sum()
total_qty = df_filtered['transaction_qty'].sum()
total_trans = df_filtered['transaction_id'].nunique()

# --- CUERPO DEL DASHBOARD ---
st.title(f"Dashboard de Ventas - {mes_seleccionado}")

# Fila 1: KPIs (Tus tarjetas de Power BI)
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Ventas", f"${total_sales:,.2f}")
with col2:
    st.metric("Cantidad Vendida", f"{total_qty:,} unidades")
with col3:
    st.metric("Total Transacciones", f"{total_trans:,}")

st.markdown("---")

# Fila 2: Gráficos principales
c1, c2 = st.columns(2)

with c1:
    st.subheader("Ventas por Categoría")
    fig_cat = px.bar(
        df_filtered.groupby('product_category')['Total_Bill'].sum().reset_index(),
        x='Total_Bill', y='product_category', orientation='h',
        color_discrete_sequence=['#6f4e37']
    )
    st.plotly_chart(fig_cat, use_container_width=True)

with c2:
    st.subheader("Ventas por Tienda")
    fig_tienda = px.pie(
        df_filtered, values='Total_Bill', names='store_location',
        hole=0.5, color_discrete_sequence=['#3d2b1f', '#6f4e37', '#c3a689']
    )
    st.plotly_chart(fig_tienda, use_container_width=True)

# Fila 3: Tabla Detallada
st.subheader("Detalle de Productos")
tabla_resumen = df_filtered.groupby('product_type').agg({
    'Total_Bill': 'sum',
    'transaction_qty': 'sum',
    'unit_price': 'mean'
}).rename(columns={'Total_Bill': 'Ventas', 'transaction_qty': 'Cantidad', 'unit_price': 'Precio Prom.'})

st.dataframe(tabla_resumen.style.format("${:,.2f}"), use_container_width=True)