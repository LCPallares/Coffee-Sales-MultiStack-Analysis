import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Coffee Shop Sales Analysis", layout="wide")

# --- 2. ESTILO CSS (Fix para KPIs y Colores) ---
st.markdown("""
    <style>
    [data-testid="stSidebar"] { background-color: #3d2b1f; }

    /* Fondo de la página */
    .main {
        background-color: #fdf5e6;
    }
    
    /* Estilo de las tarjetas de métricas */
    /* .stMetric { background-color: #fdf5e6; padding: 15px; border-radius: 10px; } */

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
        padding: 15px;
        border-radius: 10px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. CARGA DE DATOS ---
@st.cache_data
def load_data():
    # Ajusta la ruta si es necesario
    df = pd.read_csv("../Data/coffee_shop_sales.csv")
    df['transaction_date'] = pd.to_datetime(df['transaction_date'], dayfirst=True)
    df['Month_Name'] = df['transaction_date'].dt.month_name()
    df['Day'] = df['transaction_date'].dt.day 
    return df

df = load_data()

# --- 4. FUNCIONES DE VISUALIZACIÓN ---

def ventas_categorias_productos(df_filtered):
    st.subheader("Ventas por Categoría")
    fig_cat = px.bar(
        df_filtered.groupby('product_category')['Total_Bill'].sum().sort_values(ascending=True).reset_index(),
        x='Total_Bill', y='product_category', orientation='h',
        color_discrete_sequence=['#6f4e37'],
        template="simple_white"
    )
    st.plotly_chart(fig_cat, use_container_width=True)

def ventas_tiendas(df_filtered):
    st.subheader("% Ventas por Tienda")
    fig_pie = px.pie(
        df_filtered, values='Total_Bill', names='store_location',
        hole=0.5,
        color_discrete_sequence=['#3d2b1f', '#6f4e37', '#c3a689']
    )
    st.plotly_chart(fig_pie, use_container_width=True)

def ventas_mes_con_promedio(df_all):
    st.subheader("Tendencia Mensual")
    meses_ordenados = ["January", "February", "March", "April", "May", "June"]
    df_mensual = df_all.groupby('Month_Name')['Total_Bill'].sum().reindex(meses_ordenados).reset_index()
    promedio_ventas = df_mensual['Total_Bill'].mean()

    fig_mes = go.Figure()
    fig_mes.add_trace(go.Bar(
        x=df_mensual['Month_Name'], y=df_mensual['Total_Bill'],
        marker_color='#6f4e37',
        text=[f"${val:,.0f}" for val in df_mensual['Total_Bill']],
        textposition='auto'
    ))
    fig_mes.add_hline(y=promedio_ventas, line_dash="dot", line_color="#3d2b1f", 
                      annotation_text=f"Promedio: ${promedio_ventas:,.0f}")
    fig_mes.update_layout(plot_bgcolor='rgba(0,0,0,0)', height=400)
    st.plotly_chart(fig_mes, use_container_width=True)

def tabla_categoria(df_filtered):
    st.subheader("Resumen Ejecutivo")
    resumen = df_filtered.groupby('product_category').agg({
        'Total_Bill': 'sum',
        'unit_price': 'mean',
        'transaction_qty': 'sum'
    }).reset_index()
    total_v = resumen['Total_Bill'].sum()
    resumen['% sales'] = (resumen['Total_Bill'] / total_v) * 100
    st.dataframe(resumen.style.format({
        'Total_Bill': '${:,.2f}', 'unit_price': '${:,.2f}',
        '% sales': '{:.2f}%', 'transaction_qty': '{:,}'
    }), use_container_width=True)

def kpis_mensuales_comparativos(df_act, df_ant):
    c1, c2, c3 = st.columns(3)
    def calc_delta(act, ant):
        return ((act - ant) / ant) * 100 if ant > 0 else 0

    with c1:
        v_act, v_ant = df_act['Total_Bill'].sum(), df_ant['Total_Bill'].sum() if not df_ant.empty else 0
        st.metric("Ventas Totales", f"${v_act:,.2f}", f"{calc_delta(v_act, v_ant):.2f}% vs PM")
    with c2:
        q_act, q_ant = df_act['transaction_qty'].sum(), df_ant['transaction_qty'].sum() if not df_ant.empty else 0
        st.metric("Cantidad Vendida", f"{q_act:,}", f"{calc_delta(q_act, q_ant):.2f}% vs PM")
    with c3:
        t_act, t_ant = df_act['transaction_id'].nunique(), df_ant['transaction_id'].nunique() if not df_ant.empty else 0
        st.metric("Transacciones", f"{t_act:,}", f"{calc_delta(t_act, t_ant):.2f}% vs PM")

# --- 5. SIDEBAR (Navegación y Filtros) ---
st.sidebar.title("☕ Coffee Analytics")
pagina = st.sidebar.radio("Navegación:", ["Overview", "Monthly Sales"])
st.sidebar.markdown("---")

meses_disponibles = ["Todas"] + ["January", "February", "March", "April", "May", "June"]
mes_seleccionado = st.sidebar.selectbox("Filtrar por Mes:", meses_disponibles)

tiendas_disponibles = ["Todas"] + list(df['store_location'].unique())
tienda_seleccionada = st.sidebar.selectbox("Filtrar por Tienda:", tiendas_disponibles)

# Lógica de filtrado
df_filtered = df.copy()
if mes_seleccionado != "Todas":
    df_filtered = df_filtered[df_filtered['Month_Name'] == mes_seleccionado]
if tienda_seleccionada != "Todas":
    df_filtered = df_filtered[df_filtered['store_location'] == tienda_seleccionada]

# --- 6. RENDERIZADO DE PÁGINAS ---

if pagina == "Overview":
    st.title("📊 Vista General del Negocio")
    
    # KPIs Rápidos
    col1, col2, col3 = st.columns(3)
    col1.metric("Ingresos", f"${df_filtered['Total_Bill'].sum():,.2f}")
    col2.metric("Unidades", f"{df_filtered['transaction_qty'].sum():,}")
    col3.metric("Tickets", f"{df_filtered['transaction_id'].nunique():,}")
    
    st.markdown("---")
    c1, c2 = st.columns([6, 4])
    with c1: ventas_categorias_productos(df_filtered)
    with c2: ventas_tiendas(df_filtered)
    
    ventas_mes_con_promedio(df) # Siempre pasamos df completo para ver la tendencia
    tabla_categoria(df_filtered)

elif pagina == "Monthly Sales":
    if mes_seleccionado == "Todas":
        st.warning("Selecciona un mes en el sidebar para ver el análisis comparativo.")
    else:
        st.title(f"📈 Análisis Detallado: {mes_seleccionado}")
        
        # Obtener mes anterior para deltas
        meses_lista = ["January", "February", "March", "April", "May", "June"]
        idx = meses_lista.index(mes_seleccionado)
        mes_ant_nombre = meses_lista[idx - 1] if idx > 0 else None
        df_ant = df[df['Month_Name'] == mes_ant_nombre] if mes_ant_nombre else pd.DataFrame()
        
        kpis_mensuales_comparativos(df_filtered, df_ant)
        st.markdown("---")
        
        # Gráfico diario (Replica de tu Imagen 1)
        daily = df_filtered.groupby('Day')['Total_Bill'].sum().reset_index()
        fig_d = px.bar(daily, x='Day', y='Total_Bill', title="Ventas Diarias", color_discrete_sequence=['#c3a689'])
        fig_d.add_hline(y=daily['Total_Bill'].mean(), line_dash="dot", line_color="#3d2b1f")
        st.plotly_chart(fig_d, use_container_width=True)