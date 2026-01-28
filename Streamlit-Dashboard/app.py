import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Coffee Shop Sales Analysis", layout="wide")

# Estilo personalizado para el sidebar y colores (opcional)
st.markdown("""
    <style>
    [data-testid="stSidebar"] { background-color: #3d2b1f; }
    .stMetric { background-color: #fdf5e6; padding: 15px; border-radius: 10px; }

    /* Fondo de la página */
    .main {
        background-color: #fdf5e6;
    }
    
    /* Estilo de las tarjetas de métricas */
    [data-testid="stMetricValue"] {
        color: #3d2b1f !important; /* Texto oscuro para el valor */
        font-weight: bold;
    }
    [data-testid="stMetricLabel"] {
        color: #6f4e37 !important; /* Texto café para la etiqueta */
    }
    div[data-testid="metric-container"] {
        background-color: #ffffff; /* Fondo blanco/crema para la tarjeta */
        border: 1px solid #c3a689;
        padding: 15px 15px 15px 25px;
        border-radius: 10px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    }

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


def ventas_categorias_productos(df):
    st.subheader("Ventas por Categoría de Producto")
    # Gráfico de barras horizontales como en tu imagen
    fig_cat = px.bar(
        df_filtered.groupby('product_category')['Total_Bill'].sum().sort_values(ascending=True).reset_index(),
        x='Total_Bill', y='product_category', orientation='h',
        color_discrete_sequence=['#6f4e37'],
        template="simple_white"
    )
    st.plotly_chart(fig_cat, use_container_width=True)

def ventas_tiendas(df):
    st.subheader("% Ventas por Tienda")
    fig_pie = px.pie(
        df_filtered, values='Total_Bill', names='store_location',
        hole=0.5,
        color_discrete_sequence=['#3d2b1f', '#6f4e37', '#c3a689']
    )
    st.plotly_chart(fig_pie, use_container_width=True)

def ventas_mes(df):
    # --- GRÁFICA DE VENTAS POR MES CON LÍNEA DE PROMEDIO ---
    st.subheader("Ventas por Mes")

    # 1. Preparar los datos (Agrupamos por el nombre del mes)
    # Ordenamos por fecha para que los meses aparezcan en orden cronológico
    meses_ordenados = ["January", "February", "March", "April", "May", "June"]
    df_mensual = df.groupby('Month_Name')['Total_Bill'].sum().reindex(meses_ordenados).reset_index()

    # 2. Calcular el promedio global
    promedio_ventas = df_mensual['Total_Bill'].mean()

    # 3. Crear la figura con Graph Objects para mayor control
    fig_mes = go.Figure()

    # Añadir las barras (Ventas)
    fig_mes.add_trace(go.Bar(
        x=df_mensual['Month_Name'],
        y=df_mensual['Total_Bill'],
        name='Ventas Mensuales',
        marker_color='#6f4e37', # Color café de tu paleta
        text=[f"${val:,.0f}" for val in df_mensual['Total_Bill']], # Etiquetas sobre las barras
        textposition='auto'
    ))

    # Añadir la línea de promedio (Igual a la de tu Imagen 0)
    fig_mes.add_hline(
        y=promedio_ventas, 
        line_dash="dot",
        line_color="#3d2b1f", 
        annotation_text=f"Promedio: ${promedio_ventas:,.0f}", 
        annotation_position="top left"
    )

    # Ajustar el diseño (quitar fondos, ajustar ejes)
    fig_mes.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis_title="",
        yaxis_title="Suma de Total_Bill",
        margin=dict(l=20, r=20, t=30, b=20),
        height=400
    )

    st.plotly_chart(fig_mes, use_container_width=True)

def tabla_categoria(df):
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
    ventas_categorias_productos(df_filtered)

with c2:
    ventas_tiendas(df_filtered)

ventas_mes(df_filtered)

# Fila 3: Tabla de Resumen Global (La que tienes abajo a la derecha en la Imagen 0)
tabla_categoria(df_filtered)
