import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- CONFIGURACIÓN Y ESTILO ---
st.set_page_config(page_title="Coffee Shop Sales Analysis", layout="wide")

st.markdown("""
    <style>
    [data-testid="stSidebar"] { background-color: #3d2b1f; }
    .main { background-color: #fdf5e6; }
    [data-testid="stMetricValue"] { color: #3d2b1f !important; font-weight: bold; }
    [data-testid="stMetricLabel"] { color: #6f4e37 !important; }
    div[data-testid="metric-container"] {
        background-color: #ffffff;
        border: 1px solid #c3a689;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

# --- CARGA DE DATOS ---
@st.cache_data
def load_data():
    df = pd.read_csv("../Data/coffee_shop_sales.csv")
    df['transaction_date'] = pd.to_datetime(df['transaction_date'], dayfirst=True)

    df['Month_Name'] = df['transaction_date'].dt.month_name()
    df['Day'] = df['transaction_date'].dt.day
    #df['Hour'] = df['transaction_date'].dt.hour
    #df['transaction_time'] = pd.to_datetime(df['transaction_time'])
    #df['Hour'] = df['transaction_time'].dt.hour  # ya tenemos columna hora
    df['Day_Name'] = df['transaction_date'].dt.day_name()

    # Mantenemos Total_Bill como numérico por si acaso
    df['Total_Bill'] = df['unit_price'] * df['transaction_qty']
    return df

df = load_data()

# --- FUNCIONES DE VISUALIZACIÓN ---

def metricas_kpi(df_filtered, df_ant=None):
    col1, col2, col3 = st.columns(3)
    
    def calc_delta(act, ant):
        return ((act - ant) / ant) * 100 if ant is not None and ant > 0 else None

    v_act = df_filtered['Total_Bill'].sum()
    q_act = df_filtered['transaction_qty'].sum()
    t_act = df_filtered['transaction_id'].nunique()

    v_ant = df_ant['Total_Bill'].sum() if df_ant is not None and not df_ant.empty else None
    q_ant = df_ant['transaction_qty'].sum() if df_ant is not None and not df_ant.empty else None
    t_ant = df_ant['transaction_id'].nunique() if df_ant is not None and not df_ant.empty else None

    with col1:
        st.metric("Ventas Totales", f"${v_act:,.2f}", f"{calc_delta(v_act, v_ant):.2f}%" if v_ant else None)
    with col2:
        st.metric("Cantidad Vendida", f"{q_act:,}", f"{calc_delta(q_act, q_ant):.2f}%" if q_ant else None)
    with col3:
        st.metric("Total Transacciones", f"{t_act:,}", f"{calc_delta(t_act, t_ant):.2f}%" if t_ant else None)

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

def ventas_mensuales_tendencia(df_all):
    st.subheader("Tendencia Mensual Global")
    meses_ordenados = ["January", "February", "March", "April", "May", "June"]
    df_mensual = df_all.groupby('Month_Name')['Total_Bill'].sum().reindex(meses_ordenados).reset_index()
    promedio = df_mensual['Total_Bill'].mean()
    
    colores = ['#59270E' if val >= promedio else '#c3a689' for val in df_mensual['Total_Bill']]
    
    fig = go.Figure()
    fig.add_trace(go.Bar(x=df_mensual['Month_Name'], y=df_mensual['Total_Bill'], marker_color=colores))
    fig.add_hline(y=promedio, line_dash="dot", line_color="#3d2b1f")
    fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', height=400)
    st.plotly_chart(fig, use_container_width=True)

def ventas_diarias_barra(df_filtered, mes_nombre):
    st.subheader(f"Ventas por Día - {mes_nombre}")
    daily = df_filtered.groupby('Day')['Total_Bill'].sum().reset_index()
    avg_val = daily['Total_Bill'].mean()
    colores = ['#59270E' if val >= avg_val else '#c3a689' for val in daily['Total_Bill']]
    
    fig = go.Figure()
    fig.add_trace(go.Bar(x=daily['Day'], y=daily['Total_Bill'], marker_color=colores))
    fig.add_hline(y=avg_val, line_dash="dot", line_color="#3d2b1f", annotation_text=f"Promedio: ${avg_val:,.0f}")
    fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', height=400)
    st.plotly_chart(fig, use_container_width=True)

def ventas_variacion_categoria(df_actual, df_anterior):
    st.subheader("Variación de Ventas vs Mes Anterior ($)")
    
    if df_anterior.empty:
        st.info("No hay datos del mes anterior para comparar.")
        return

    # 1. Calcular ventas por categoría para ambos meses
    cat_act = df_actual.groupby('product_category')['Total_Bill'].sum()
    cat_ant = df_anterior.groupby('product_category')['Total_Bill'].sum()
    
    # 2. Crear DataFrame de comparación
    df_diff = pd.DataFrame({
        'Actual': cat_act,
        'Anterior': cat_ant
    }).fillna(0)
    
    df_diff['Diferencia'] = df_diff['Actual'] - df_diff['Anterior']
    df_diff = df_diff.sort_values('Diferencia', ascending=True).reset_index()
    
    # 3. Lógica de color: Café oscuro para positivo, Gris/Crema para negativo
    df_diff['Color'] = ['#59270E' if x > 0 else '#c3a689' for x in df_diff['Diferencia']]
    
    fig_diff = px.bar(
        df_diff, 
        x='Diferencia', 
        y='product_category', 
        orientation='h',
        title="Diferencia Nominal en Ventas",
        text='Diferencia'
    )
    
    fig_diff.update_traces(
        marker_color=df_diff['Color'],
        texttemplate='%{text:$.2s}', # Formato de moneda abreviado (k)
        textposition='outside'
    )
    
    fig_diff.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis_title="Diferencia en USD",
        yaxis_title="",
        height=400
    )
    
    st.plotly_chart(fig_diff, use_container_width=True)

def ventas_comparativas_categoria(df_actual, df_anterior):
    st.subheader("Comparativa de Ventas: Mes Actual vs Mes Anterior")
    
    if df_anterior.empty:
        st.info("Selecciona un mes a partir de Febrero para ver la comparativa con el mes anterior.")
        return

    # 1. Agrupar ventas por categoría para ambos periodos
    cat_act = df_actual.groupby('product_category')['Total_Bill'].sum().reset_index()
    cat_ant = df_anterior.groupby('product_category')['Total_Bill'].sum().reset_index()
    
    # 2. Unir ambos dataframes
    df_comp = pd.merge(cat_act, cat_ant, on='product_category', how='outer', suffixes=('_Actual', '_Anterior')).fillna(0)
    df_comp = df_comp.sort_values('Total_Bill_Actual', ascending=True)

    # 3. Crear el gráfico de barras agrupadas
    fig = go.Figure()

    # Barra Mes Anterior (Color claro)
    fig.add_trace(go.Bar(
        y=df_comp['product_category'],
        x=df_comp['Total_Bill_Anterior'],
        name='Mes Anterior',
        orientation='h',
        marker_color='#c3a689'
    ))

    # Barra Mes Actual (Color oscuro)
    fig.add_trace(go.Bar(
        y=df_comp['product_category'],
        x=df_comp['Total_Bill_Actual'],
        name='Mes Actual',
        orientation='h',
        marker_color='#59270E'
    ))

    # 4. Configurar el diseño
    fig.update_layout(
        barmode='group', # Esto hace que las barras se agrupen una al lado de la otra
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis_title="Ventas ($)",
        yaxis_title="",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        height=500,
        margin=dict(l=0, r=0, t=30, b=0)
    )

    st.plotly_chart(fig, use_container_width=True)

def tabla_resumen(df_filtered):
    st.subheader("Resumen Ejecutivo de Categorías")
    resumen = df_filtered.groupby('product_category').agg({'Total_Bill': 'sum', 'unit_price': 'mean', 'transaction_qty': 'sum'}).reset_index()
    resumen['% sales'] = (resumen['Total_Bill'] / resumen['Total_Bill'].sum()) * 100
    st.dataframe(resumen.style.format({'Total_Bill': '${:,.2f}', 'unit_price': '${:,.2f}', '% sales': '{:.2f}%'}), use_container_width=True)

def mapa_calor_horarios(df_filtered):
    st.subheader("Patrón de Tráfico: Horas vs. Días de la Semana")
    st.subheader(f"hora: {df_filtered['Hour']}")
    
    # 1. Preparar los datos: Tabla pivote
    # Ordenamos los días para que no salgan alfabéticos
    orden_dias = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    
    pivot_table = df_filtered.pivot_table(
        index='Hour',
        columns='Day Name',
        values='Total_Bill',
        aggfunc='sum'
    ).reindex(columns=orden_dias)

    # 2. Crear el Heatmap con Plotly
    fig = px.imshow(
        pivot_table,
        labels=dict(x="Día de la Semana", y="Hora del Día", color="Ventas ($)"),
        x=pivot_table.columns,
        y=pivot_table.index,
        # Escala de colores: de crema a café oscuro
        color_continuous_scale=[[0, '#fdf5e6'], [0.5, '#c3a689'], [1, '#59270E']]
    )

    fig.update_layout(
        xaxis_title="",
        yaxis_title="Hora (formato 24h)",
        coloraxis_showscale=True,
        height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)

def top_productos_barra(df_filtered):
    st.subheader("Top 10 Productos por Volumen")
    top_productos = df_filtered.groupby('product_type')['transaction_qty'].sum().sort_values(ascending=False).head(10).reset_index()
    
    # Cambiamos marker_color por color_discrete_sequence
    fig_top = px.bar(
        top_productos, 
        x='transaction_qty', 
        y='product_type', 
        orientation='h', 
        color_discrete_sequence=['#6f4e37'], # <--- Fix aplicado
        template="simple_white"
    )
    
    # Para que el top 1 aparezca arriba
    fig_top.update_layout(yaxis={'categoryorder':'total ascending'})
    
    st.plotly_chart(fig_top, use_container_width=True)


# --- NAVEGACIÓN Y FILTROS ---
pagina = st.sidebar.radio("Navegación:", ["Overview", "Monthly Sales", "Shopper Behavior"])
meses_lista = ["January", "February", "March", "April", "May", "June"]
mes_seleccionado = st.sidebar.selectbox("Mes:", ["Todas"] + meses_lista)

df_filtered = df.copy()
if mes_seleccionado != "Todas":
    df_filtered = df_filtered[df_filtered['Month_Name'] == mes_seleccionado]

# --- RENDER ---
if pagina == "Overview":
    st.title("📊 Coffee Overview")
    metricas_kpi(df_filtered)
    st.markdown("---")
    c1, c2 = st.columns([6, 4])
    with c1: ventas_categorias_productos(df_filtered)
    with c2: ventas_tiendas(df_filtered)
    ventas_mensuales_tendencia(df)
    tabla_resumen(df_filtered)

elif pagina == "Monthly Sales":
    if mes_seleccionado == "Todas":
        st.warning("Selecciona un mes para ver el detalle.")
    else:
        st.title(f"📈 Análisis Detallado: {mes_seleccionado}")
        
        # Obtener mes anterior (Ya lo tienes en tu código)
        idx = meses_lista.index(mes_seleccionado)
        df_ant = df[df['Month_Name'] == meses_lista[idx-1]] if idx > 0 else pd.DataFrame()
        
        metricas_kpi(df_filtered, df_ant)
        
        st.markdown("---")
        
        # Fila de gráficas
        col_izq, col_der = st.columns([1, 1])
        with col_izq:
            ventas_diarias_barra(df_filtered, mes_seleccionado)
        with col_der:
            # Llamamos a la nueva función de dos barras por categoría
            ventas_comparativas_categoria(df_filtered, df_ant)
            
        tabla_resumen(df_filtered)

elif pagina == "Shopper Behavior":
    st.title("👥 Comportamiento del Consumidor")
    
    # KPIs Rápidos (siempre útiles)
    metricas_kpi(df_filtered)
    st.markdown("---")
    
    # El Heatmap ocupa el ancho total
    mapa_calor_horarios(df_filtered)
    
    # Fila adicional: Productos más vendidos en esta selección
    top_productos_barra(df_filtered)
