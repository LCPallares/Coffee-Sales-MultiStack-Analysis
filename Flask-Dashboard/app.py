from flask import Flask, render_template, request, jsonify
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import os
import json
import plotly

app = Flask(__name__)

# --- CARGA DE DATOS ---
def load_data():
    base_path = os.path.dirname(__file__)
    file_path = os.path.join(base_path, "data", "coffee_shop_sales.csv")
    df = pd.read_csv(file_path)

    df['transaction_date'] = pd.to_datetime(df['transaction_date'], dayfirst=True)
    df['Month_Name'] = df['transaction_date'].dt.month_name()
    df['Day'] = df['transaction_date'].dt.day
    df['Day_Name'] = df['transaction_date'].dt.day_name()
    df['Total_Bill'] = df['unit_price'] * df['transaction_qty']
    
    return df

# Cargar datos al inicio
df = load_data()

# --- FUNCIONES AUXILIARES ---
def get_filtered_data(month_name=None):
    if month_name and month_name != "Todas":
        return df[df['Month_Name'] == month_name].copy()
    return df.copy()

def get_previous_month_data(month_name):
    meses_lista = ["January", "February", "March", "April", "May", "June"]
    if month_name in meses_lista:
        idx = meses_lista.index(month_name)
        if idx > 0:
            return df[df['Month_Name'] == meses_lista[idx-1]].copy()
    return pd.DataFrame()

def calc_delta(act, ant):
    return ((act - ant) / ant) * 100 if ant is not None and ant > 0 else None

def get_kpi_metrics(df_filtered, df_ant=None):
    v_act = df_filtered['Total_Bill'].sum()
    q_act = df_filtered['transaction_qty'].sum()
    t_act = df_filtered['transaction_id'].nunique()

    v_ant = df_ant['Total_Bill'].sum() if df_ant is not None and not df_ant.empty else None
    q_ant = df_ant['transaction_qty'].sum() if df_ant is not None and not df_ant.empty else None
    t_ant = df_ant['transaction_id'].nunique() if df_ant is not None and not df_ant.empty else None

    metrics = {
        'ventas': {
            'value': v_act,
            'delta': calc_delta(v_act, v_ant) if v_ant else None
        },
        'cantidad': {
            'value': q_act,
            'delta': calc_delta(q_act, q_ant) if q_ant else None
        },
        'transacciones': {
            'value': t_act,
            'delta': calc_delta(t_act, t_ant) if t_ant else None
        }
    }
    return metrics

# --- FUNCIONES DE GRÁFICOS ---
def create_ventas_categorias(df_filtered):
    fig_cat = px.bar(
        df_filtered.groupby('product_category')['Total_Bill'].sum().sort_values(ascending=True).reset_index(),
        x='Total_Bill', y='product_category', orientation='h',
        color_discrete_sequence=['#6f4e37'],
        template="simple_white"
    )
    return json.dumps(fig_cat, cls=plotly.utils.PlotlyJSONEncoder)

def create_ventas_tiendas(df_filtered):
    fig_pie = px.pie(
        df_filtered, values='Total_Bill', names='store_location',
        hole=0.5,
        color_discrete_sequence=['#3d2b1f', '#6f4e37', '#c3a689']
    )
    return json.dumps(fig_pie, cls=plotly.utils.PlotlyJSONEncoder)

def create_ventas_mensuales(df_all):
    meses_ordenados = ["January", "February", "March", "April", "May", "June"]
    df_mensual = df_all.groupby('Month_Name')['Total_Bill'].sum().reindex(meses_ordenados).reset_index()
    promedio = df_mensual['Total_Bill'].mean()
    
    colores = ['#59270E' if val >= promedio else '#c3a689' for val in df_mensual['Total_Bill']]
    
    fig = go.Figure()
    fig.add_trace(go.Bar(x=df_mensual['Month_Name'], y=df_mensual['Total_Bill'], marker_color=colores))
    fig.add_hline(y=promedio, line_dash="dot", line_color="#3d2b1f")
    fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', height=400)
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

def create_ventas_diarias(df_filtered):
    daily = df_filtered.groupby('Day')['Total_Bill'].sum().reset_index()
    avg_val = daily['Total_Bill'].mean()
    colores = ['#59270E' if val >= avg_val else '#c3a689' for val in daily['Total_Bill']]
    
    fig = go.Figure()
    fig.add_trace(go.Bar(x=daily['Day'], y=daily['Total_Bill'], marker_color=colores))
    fig.add_hline(y=avg_val, line_dash="dot", line_color="#3d2b1f", 
                  annotation_text=f"Promedio: ${avg_val:,.0f}")
    fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', height=400)
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

def create_comparativa_categorias(df_actual, df_anterior):
    if df_anterior.empty:
        return None
    
    cat_act = df_actual.groupby('product_category')['Total_Bill'].sum().reset_index()
    cat_ant = df_anterior.groupby('product_category')['Total_Bill'].sum().reset_index()
    
    df_comp = pd.merge(cat_act, cat_ant, on='product_category', how='outer', 
                       suffixes=('_Actual', '_Anterior')).fillna(0)
    df_comp = df_comp.sort_values('Total_Bill_Actual', ascending=True)

    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=df_comp['product_category'],
        x=df_comp['Total_Bill_Anterior'],
        name='Mes Anterior',
        orientation='h',
        marker_color='#c3a689'
    ))
    fig.add_trace(go.Bar(
        y=df_comp['product_category'],
        x=df_comp['Total_Bill_Actual'],
        name='Mes Actual',
        orientation='h',
        marker_color='#59270E'
    ))

    fig.update_layout(
        barmode='group',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis_title="Ventas ($)",
        yaxis_title="",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        height=500,
        margin=dict(l=0, r=0, t=30, b=0)
    )
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

def create_mapa_calor(df_filtered):
    orden_dias = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    
    pivot_table = df_filtered.pivot_table(
        index='Hour',
        columns='Day_Name',
        values='Total_Bill',
        aggfunc='sum'
    ).reindex(columns=orden_dias).fillna(0)

    fig_heat = px.imshow(
        pivot_table,
        labels=dict(x="", y="Hora", color="Ventas ($)"),
        x=pivot_table.columns,
        y=pivot_table.index,
        color_continuous_scale=[[0, '#fdf5e6'], [0.5, '#c3a689'], [1, '#59270E']]
    )
    
    fig_heat.update_layout(height=400, margin=dict(b=0))
    return json.dumps(fig_heat, cls=plotly.utils.PlotlyJSONEncoder)

def create_totales_dia(df_filtered):
    orden_dias = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    totales_dia = df_filtered.groupby('Day_Name')['Total_Bill'].sum().reindex(orden_dias).reset_index()
    promedio = totales_dia['Total_Bill'].mean()
    
    colores = ['#59270E' if x >= promedio else '#c3a689' for x in totales_dia['Total_Bill']]

    fig_bar = go.Figure()
    fig_bar.add_trace(go.Bar(
        x=totales_dia['Day_Name'],
        y=totales_dia['Total_Bill'],
        marker_color=colores,
        text=[f"${x:,.0f}" for x in totales_dia['Total_Bill']],
        textposition='outside',
        cliponaxis=False
    ))

    fig_bar.update_layout(
        height=200,
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(t=50, b=0),
        xaxis_title="",
        yaxis_title="Total Día",
        showlegend=False
    )
    fig_bar.update_yaxes(visible=False)
    
    return json.dumps(fig_bar, cls=plotly.utils.PlotlyJSONEncoder)

def create_matriz_estrategica(df_filtered):
    cat_analisis = df_filtered.groupby('product_category').agg({
        'unit_price': 'mean',
        'transaction_qty': 'mean',
        'Total_Bill': 'sum'
    }).reset_index()

    avg_price = cat_analisis['unit_price'].mean()
    avg_qty = cat_analisis['transaction_qty'].mean()

    fig = px.scatter(
        cat_analisis, 
        x='unit_price', 
        y='transaction_qty',
        size='Total_Bill',
        color='product_category',
        hover_name='product_category',
        text='product_category',
        labels={
            'unit_price': 'Precio Unitario Promedio ($)',
            'transaction_qty': 'Cant. Promedio por Transacción'
        },
        color_discrete_sequence=px.colors.qualitative.Antique
    )

    fig.add_vline(x=avg_price, line_dash="dash", line_color="#3d2b1f", opacity=0.5)
    fig.add_hline(y=avg_qty, line_dash="dash", line_color="#3d2b1f", opacity=0.5)

    fig.update_traces(textposition='top center')
    fig.update_layout(
        height=600,
        plot_bgcolor='rgba(0,0,0,0)',
        showlegend=False
    )
    
    fig.add_annotation(x=cat_analisis['unit_price'].max(), y=cat_analisis['transaction_qty'].max(),
                text="Premium / High Volume", showarrow=False, opacity=0.3)
    fig.add_annotation(x=cat_analisis['unit_price'].min(), y=cat_analisis['transaction_qty'].min(),
                text="Underperformers", showarrow=False, opacity=0.3)

    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder), avg_price, avg_qty

def create_analisis_precio(df_filtered):
    precio_analisis = df_filtered.groupby('unit_price').agg({
        'transaction_id': 'nunique',
        'transaction_qty': 'sum'
    }).reset_index()

    fig = px.scatter(
        precio_analisis, 
        x='unit_price', 
        y='transaction_id',
        size='transaction_qty',
        hover_name='unit_price',
        color_discrete_sequence=['#59270E'],
        labels={
            'unit_price': 'Precio Unitario ($)',
            'transaction_id': 'Número de Transacciones'
        },
        template="simple_white"
    )

    fig.update_layout(
        height=450,
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

def create_top_productos(df_filtered):
    top_productos = df_filtered.groupby('product_type')['transaction_qty'].sum().sort_values(
        ascending=False).head(10).reset_index()
    
    fig_top = px.bar(
        top_productos, 
        x='transaction_qty', 
        y='product_type', 
        orientation='h', 
        color_discrete_sequence=['#6f4e37'],
        template="simple_white"
    )
    
    fig_top.update_layout(yaxis={'categoryorder':'total ascending'})
    
    return json.dumps(fig_top, cls=plotly.utils.PlotlyJSONEncoder)

def create_distribucion_temporal(df_all):
    df_temporal = df_all.groupby(['transaction_date', 'store_location'])['Total_Bill'].sum().reset_index()

    fig = px.area(
        df_temporal, 
        x="transaction_date", 
        y="Total_Bill", 
        color="store_location",
        line_group="store_location",
        color_discrete_sequence=['#3d2b1f', '#6f4e37', '#c3a689'],
        labels={'transaction_date': 'Fecha', 'Total_Bill': 'Ventas Diarias ($)'},
        template="simple_white"
    )

    fig.update_layout(
        height=500,
        hovermode="x unified",
        plot_bgcolor='rgba(0,0,0,0)',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )

    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

def create_evolucion_temporal(df_filtered):
    temporal_df = df_filtered.groupby('Day').agg({
        'Total_Bill': 'sum',
        'transaction_qty': 'sum',
        'transaction_id': 'nunique'
    }).reset_index()
    
    temporal_df['ticket_promedio'] = temporal_df['Total_Bill'] / temporal_df['transaction_id']

    fig_temporal = go.Figure()

    fig_temporal.add_trace(go.Scatter(
        x=temporal_df['Day'],
        y=temporal_df['Total_Bill'],
        mode='lines+markers',
        name='Ventas Totales ($)',
        line=dict(color='#59270E', width=3),
        marker=dict(size=8)
    ))

    fig_temporal.add_trace(go.Scatter(
        x=temporal_df['Day'],
        y=temporal_df['ticket_promedio'],
        mode='lines',
        name='Ticket Promedio ($)',
        line=dict(color='#4682B4', width=2, dash='dot'),
        yaxis='y2'
    ))

    fig_temporal.update_layout(
        title='Evolución de Ventas y Ticket Promedio por Día del Mes',
        xaxis=dict(
            title='Día del Mes',
            tickmode='linear',
            range=[1, 31]
        ),
        yaxis=dict(
            title=dict(text='Ventas Totales ($)', font=dict(color='#59270E')),
            tickfont=dict(color='#59270E'),
            gridcolor='rgba(0,0,0,0.1)'
        ),
        yaxis2=dict(
            title=dict(text='Ticket Promedio ($)', font=dict(color='#4682B4')),
            tickfont=dict(color='#4682B4'),
            anchor='x',
            overlaying='y',
            side='right',
            showgrid=False
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.05,
            xanchor="center",
            x=0.5
        ),
        plot_bgcolor='rgba(0,0,0,0)',
        height=500
    )

    return json.dumps(fig_temporal, cls=plotly.utils.PlotlyJSONEncoder)

def get_tabla_resumen(df_filtered):
    resumen = df_filtered.groupby('product_category').agg({
        'Total_Bill': 'sum', 
        'unit_price': 'mean', 
        'transaction_qty': 'sum'
    }).reset_index()
    resumen['% sales'] = (resumen['Total_Bill'] / resumen['Total_Bill'].sum()) * 100
    resumen.columns = ['Categoría', 'Ventas Totales', 'Precio Promedio', 'Cantidad Total', '% Ventas']
    return resumen.to_dict('records')

# --- RUTAS ---
@app.route('/')
def index():
    return render_template('overview.html', 
                         meses=["Todas", "January", "February", "March", "April", "May", "June"])

@app.route('/overview')
def overview():
    month = request.args.get('month', 'Todas')
    df_filtered = get_filtered_data(month)
    
    metrics = get_kpi_metrics(df_filtered)
    
    graph_categorias = create_ventas_categorias(df_filtered)
    graph_tiendas = create_ventas_tiendas(df_filtered)
    graph_mensual = create_ventas_mensuales(df)
    tabla = get_tabla_resumen(df_filtered)
    
    return render_template('overview.html',
                         meses=["Todas", "January", "February", "March", "April", "May", "June"],
                         selected_month=month,
                         metrics=metrics,
                         graph_categorias=graph_categorias,
                         graph_tiendas=graph_tiendas,
                         graph_mensual=graph_mensual,
                         tabla=tabla)

@app.route('/monthly')
def monthly():
    month = request.args.get('month', 'January')
    
    if month == 'Todas':
        return render_template('monthly.html',
                             meses=["January", "February", "March", "April", "May", "June"],
                             selected_month=month,
                             show_warning=True)
    
    df_filtered = get_filtered_data(month)
    df_anterior = get_previous_month_data(month)
    
    metrics = get_kpi_metrics(df_filtered, df_anterior)
    graph_diarias = create_ventas_diarias(df_filtered)
    graph_comparativa = create_comparativa_categorias(df_filtered, df_anterior)
    tabla = get_tabla_resumen(df_filtered)
    
    return render_template('monthly.html',
                         meses=["January", "February", "March", "April", "May", "June"],
                         selected_month=month,
                         show_warning=False,
                         metrics=metrics,
                         graph_diarias=graph_diarias,
                         graph_comparativa=graph_comparativa,
                         tabla=tabla,
                         mes_nombre=month)

@app.route('/behavior')
def behavior():
    month = request.args.get('month', 'Todas')
    df_filtered = get_filtered_data(month)
    
    metrics = get_kpi_metrics(df_filtered)
    graph_calor = create_mapa_calor(df_filtered)
    graph_totales = create_totales_dia(df_filtered)
    graph_precio = create_analisis_precio(df_filtered)
    graph_matriz, avg_price, avg_qty = create_matriz_estrategica(df_filtered)
    graph_top = create_top_productos(df_filtered)
    
    return render_template('behavior.html',
                         meses=["Todas", "January", "February", "March", "April", "May", "June"],
                         selected_month=month,
                         metrics=metrics,
                         graph_calor=graph_calor,
                         graph_totales=graph_totales,
                         graph_precio=graph_precio,
                         graph_matriz=graph_matriz,
                         graph_top=graph_top,
                         avg_price=f"{avg_price:.2f}",
                         avg_qty=f"{avg_qty:.2f}")

@app.route('/advanced')
def advanced():
    month = request.args.get('month', 'Todas')
    df_filtered = get_filtered_data(month)
    
    graph_distribucion = create_distribucion_temporal(df)
    graph_evolucion = create_evolucion_temporal(df_filtered)
    
    return render_template('advanced.html',
                         meses=["Todas", "January", "February", "March", "April", "May", "June"],
                         selected_month=month,
                         graph_distribucion=graph_distribucion,
                         graph_evolucion=graph_evolucion)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
