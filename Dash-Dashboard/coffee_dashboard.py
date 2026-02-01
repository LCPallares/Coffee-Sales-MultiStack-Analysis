"""
Dashboard de Análisis de Ventas de Coffee Shop
Desarrollado con Python Dash
"""

import dash
from dash import dcc, html, Input, Output
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
from datetime import datetime
import os

# Configuración de la aplicación
app = dash.Dash(__name__, suppress_callback_exceptions=True)
app.title = "Coffee Shop Dashboard"

# ============================================================================
# FUNCIONES DE CARGA Y PROCESAMIENTO DE DATOS
# ============================================================================

def load_data():
    """Carga los datos desde el archivo CSV en la carpeta Data"""
    # Intentar cargar desde diferentes rutas posibles
    
    possible_paths = [
        'Data/coffee_shop_sales.csv',
        './Data/sample_data.txt',
        '../Data/sample_data.txt',
        'sample_data.txt'
    ]
    
    df = None
    for path in possible_paths:
        if os.path.exists(path):
            #df = pd.read_csv(path, sep='\t')
            df = pd.read_csv(path)
            print(f"✓ Datos cargados desde: {path}")
            break
    
    if df is None:
        raise FileNotFoundError("No se encontró el archivo de datos en ninguna de las rutas esperadas")
    
    # Limpiar nombres de columnas
    df.columns = df.columns.str.strip()
    
    return df

def calculate_metrics(df):
    """Calcula las métricas principales del dashboard"""
    metrics = {
        'total_revenue': df['Total_Bill'].sum(),
        'total_transactions': len(df),
        'avg_ticket': df['Total_Bill'].mean(),
        'total_items': df['transaction_qty'].sum()
    }
    return metrics

def get_sales_by_hour(df):
    """Agrupa ventas por hora del día"""
    sales_by_hour = df.groupby('Hour')['Total_Bill'].sum().reset_index()
    sales_by_hour.columns = ['Hour', 'Total']
    sales_by_hour = sales_by_hour.sort_values('Hour')
    return sales_by_hour

def get_sales_by_day(df):
    """Agrupa ventas por día de la semana"""
    days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    sales_by_day = df.groupby('Day Name')['Total_Bill'].sum().reset_index()
    sales_by_day.columns = ['Day', 'Total']
    # Ordenar por el orden correcto de días
    sales_by_day['Day'] = pd.Categorical(sales_by_day['Day'], categories=days_order, ordered=True)
    sales_by_day = sales_by_day.sort_values('Day')
    return sales_by_day

def get_sales_by_category(df):
    """Agrupa ventas por categoría de producto"""
    sales_by_category = df.groupby('product_category')['Total_Bill'].sum().reset_index()
    sales_by_category.columns = ['Category', 'Total']
    return sales_by_category

def get_sales_by_location(df):
    """Agrupa ventas por ubicación de tienda"""
    sales_by_location = df.groupby('store_location')['Total_Bill'].sum().reset_index()
    sales_by_location.columns = ['Location', 'Total']
    sales_by_location = sales_by_location.sort_values('Total', ascending=False)
    return sales_by_location

def get_top_products(df, top_n=10):
    """Obtiene los productos más vendidos"""
    df['Product'] = df['product_type'] + ' - ' + df['product_detail']
    top_products = df.groupby('Product').agg({
        'transaction_qty': 'sum',
        'Total_Bill': 'sum'
    }).reset_index()
    top_products.columns = ['Product', 'Quantity', 'Revenue']
    top_products = top_products.sort_values('Quantity', ascending=False).head(top_n)
    return top_products

def get_sales_trend(df):
    """Obtiene la tendencia de ventas por fecha"""
    sales_trend = df.groupby('transaction_date')['Total_Bill'].sum().reset_index()
    sales_trend.columns = ['Date', 'Total']
    
    # Convertir fechas
    try:
        sales_trend['Date'] = pd.to_datetime(sales_trend['Date'], format='%d/%m/%Y', errors='coerce')
    except:
        try:
            sales_trend['Date'] = pd.to_datetime(sales_trend['Date'], format='%d-%m-%Y', errors='coerce')
        except:
            sales_trend['Date'] = pd.to_datetime(sales_trend['Date'], dayfirst=True, errors='coerce')
    
    sales_trend = sales_trend.dropna(subset=['Date'])
    sales_trend = sales_trend.sort_values('Date')
    return sales_trend

# ============================================================================
# ESTILOS Y COLORES
# ============================================================================

COLORS = {
    'background': '#0f172a',
    'card': '#1e293b',
    'card_hover': '#334155',
    'text': '#f8fafc',
    'text_muted': '#94a3b8',
    'primary': '#3b82f6',
    'primary_light': '#60a5fa',
    'secondary': '#8b5cf6',
    'success': '#10b981',
    'warning': '#f59e0b',
    'danger': '#ef4444',
    'border': '#334155'
}

# Estilos CSS
CARD_STYLE = {
    'backgroundColor': COLORS['card'],
    'borderRadius': '12px',
    'padding': '20px',
    'marginBottom': '20px',
    'border': f'1px solid {COLORS["border"]}',
    'boxShadow': '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
    'transition': 'all 0.3s ease'
}

KPI_CARD_STYLE = {
    **CARD_STYLE,
    'textAlign': 'center',
    'minHeight': '140px',
    'display': 'flex',
    'flexDirection': 'column',
    'justifyContent': 'space-between'
}

FILTER_STYLE = {
    'backgroundColor': COLORS['card'],
    'color': COLORS['text'],
    'borderRadius': '8px',
    'border': f'1px solid {COLORS["border"]}',
    'padding': '8px 12px',
    'fontSize': '14px'
}

# ============================================================================
# LAYOUT DE LA APLICACIÓN
# ============================================================================

def create_layout(df):
    """Crea el layout principal del dashboard"""
    
    # Obtener valores únicos para los filtros
    locations = ['Todas'] + sorted(df['store_location'].unique().tolist())
    months = ['Todos'] + sorted(df['Month Name'].unique().tolist())
    
    return html.Div([
        # Header
        html.Div([
            html.Div([
                html.H1([
                    html.I(className='fas fa-coffee', style={'marginRight': '15px'}),
                    'Coffee Shop Dashboard'
                ], style={
                    'color': COLORS['text'],
                    'fontSize': '32px',
                    'fontWeight': '700',
                    'margin': '0'
                }),
                html.P('Análisis de Ventas y Rendimiento', style={
                    'color': COLORS['text_muted'],
                    'margin': '5px 0 0 0',
                    'fontSize': '14px'
                })
            ], style={'flex': '1'}),
        ], style={
            'backgroundColor': COLORS['card'],
            'padding': '25px 40px',
            'marginBottom': '20px',
            'borderBottom': f'2px solid {COLORS["primary"]}',
            'display': 'flex',
            'alignItems': 'center',
            'justifyContent': 'space-between'
        }),
        
        # Filters
        html.Div([
            html.Div([
                html.Span('Filtros:', style={
                    'color': COLORS['text_muted'],
                    'fontSize': '14px',
                    'fontWeight': '600',
                    'marginRight': '20px'
                }),
                html.Div([
                    html.Label([
                        html.I(className='fas fa-map-marker-alt', 
                              style={'marginRight': '8px', 'color': COLORS['primary']}),
                        'Ubicación'
                    ], style={'color': COLORS['text'], 'fontSize': '14px', 'marginBottom': '5px'}),
                    dcc.Dropdown(
                        id='location-filter',
                        options=[{'label': loc, 'value': loc} for loc in locations],
                        value='Todas',
                        style={
                            'width': '200px',
                            'backgroundColor': COLORS['card'],
                            'color': COLORS['text']
                        },
                        className='custom-dropdown'
                    )
                ], style={'marginRight': '20px'}),
                html.Div([
                    html.Label([
                        html.I(className='fas fa-calendar', 
                              style={'marginRight': '8px', 'color': COLORS['primary']}),
                        'Mes'
                    ], style={'color': COLORS['text'], 'fontSize': '14px', 'marginBottom': '5px'}),
                    dcc.Dropdown(
                        id='month-filter',
                        options=[{'label': month, 'value': month} for month in months],
                        value='Todos',
                        style={
                            'width': '180px',
                            'backgroundColor': COLORS['card'],
                            'color': COLORS['text']
                        },
                        className='custom-dropdown'
                    )
                ])
            ], style={'display': 'flex', 'alignItems': 'flex-end', 'gap': '15px'})
        ], style={
            'backgroundColor': COLORS['card'],
            'padding': '20px 40px',
            'marginBottom': '25px',
            'borderRadius': '12px',
            'border': f'1px solid {COLORS["border"]}'
        }),
        
        # Main Content
        html.Div([
            # KPI Cards
            html.Div([
                create_kpi_card('revenue-card', 'fas fa-dollar-sign', 'Ingresos Totales', 
                              '$0', '+12.5% vs mes anterior', COLORS['primary']),
                create_kpi_card('transactions-card', 'fas fa-shopping-cart', 'Transacciones', 
                              '0', '+8.2% vs mes anterior', COLORS['success']),
                create_kpi_card('avg-ticket-card', 'fas fa-chart-line', 'Ticket Promedio', 
                              '$0', '+3.1% vs mes anterior', COLORS['secondary']),
                create_kpi_card('items-card', 'fas fa-coffee', 'Productos Vendidos', 
                              '0', '+15.3% vs mes anterior', COLORS['warning']),
            ], style={
                'display': 'grid',
                'gridTemplateColumns': 'repeat(auto-fit, minmax(240px, 1fr))',
                'gap': '20px',
                'marginBottom': '30px'
            }),
            
            # Charts Row 1
            html.Div([
                html.Div([
                    html.Div(style=CARD_STYLE, children=[
                        html.H3('Tendencia de Ventas', style={
                            'color': COLORS['text'],
                            'fontSize': '18px',
                            'fontWeight': '600',
                            'marginBottom': '5px'
                        }),
                        html.P('Ingresos diarios del período seleccionado', style={
                            'color': COLORS['text_muted'],
                            'fontSize': '13px',
                            'marginBottom': '15px'
                        }),
                        dcc.Graph(id='sales-trend-chart', config={'displayModeBar': False})
                    ])
                ], style={'flex': '1'}),
                html.Div([
                    html.Div(style=CARD_STYLE, children=[
                        html.H3('Ventas por Hora', style={
                            'color': COLORS['text'],
                            'fontSize': '18px',
                            'fontWeight': '600',
                            'marginBottom': '5px'
                        }),
                        html.P('Distribución de ventas durante el día', style={
                            'color': COLORS['text_muted'],
                            'fontSize': '13px',
                            'marginBottom': '15px'
                        }),
                        dcc.Graph(id='sales-by-hour-chart', config={'displayModeBar': False})
                    ])
                ], style={'flex': '1'})
            ], style={
                'display': 'flex',
                'gap': '20px',
                'marginBottom': '30px',
                'flexWrap': 'wrap'
            }),
            
            # Charts Row 2
            html.Div([
                html.Div([
                    html.Div(style=CARD_STYLE, children=[
                        html.H3('Ventas por Categoría', style={
                            'color': COLORS['text'],
                            'fontSize': '18px',
                            'fontWeight': '600',
                            'marginBottom': '5px'
                        }),
                        html.P('Distribución por tipo de producto', style={
                            'color': COLORS['text_muted'],
                            'fontSize': '13px',
                            'marginBottom': '15px'
                        }),
                        dcc.Graph(id='sales-by-category-chart', config={'displayModeBar': False})
                    ])
                ], style={'flex': '1'}),
                html.Div([
                    html.Div(style=CARD_STYLE, children=[
                        html.H3('Ventas por Día', style={
                            'color': COLORS['text'],
                            'fontSize': '18px',
                            'fontWeight': '600',
                            'marginBottom': '5px'
                        }),
                        html.P('Rendimiento semanal', style={
                            'color': COLORS['text_muted'],
                            'fontSize': '13px',
                            'marginBottom': '15px'
                        }),
                        dcc.Graph(id='sales-by-day-chart', config={'displayModeBar': False})
                    ])
                ], style={'flex': '1'}),
                html.Div([
                    html.Div(style=CARD_STYLE, children=[
                        html.H3('Ventas por Tienda', style={
                            'color': COLORS['text'],
                            'fontSize': '18px',
                            'fontWeight': '600',
                            'marginBottom': '5px'
                        }),
                        html.P('Comparación de ubicaciones', style={
                            'color': COLORS['text_muted'],
                            'fontSize': '13px',
                            'marginBottom': '15px'
                        }),
                        dcc.Graph(id='sales-by-location-chart', config={'displayModeBar': False})
                    ])
                ], style={'flex': '1'})
            ], style={
                'display': 'flex',
                'gap': '20px',
                'marginBottom': '30px',
                'flexWrap': 'wrap'
            }),
            
            # Top Products
            html.Div(style=CARD_STYLE, children=[
                html.H3('Productos Más Vendidos', style={
                    'color': COLORS['text'],
                    'fontSize': '18px',
                    'fontWeight': '600',
                    'marginBottom': '5px'
                }),
                html.P('Top 10 productos por cantidad vendida', style={
                    'color': COLORS['text_muted'],
                    'fontSize': '13px',
                    'marginBottom': '15px'
                }),
                dcc.Graph(id='top-products-chart', config={'displayModeBar': False})
            ])
        ], style={'padding': '0 40px 40px 40px'}),
        
        # Hidden div to store filtered data
        html.Div(id='filtered-data', style={'display': 'none'})
        
    ], style={
        'backgroundColor': COLORS['background'],
        'minHeight': '100vh',
        'fontFamily': '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif'
    })

def create_kpi_card(id, icon, title, value, change, color):
    """Crea una tarjeta KPI"""
    return html.Div([
        html.Div([
            html.Div([
                html.I(className=icon, style={
                    'fontSize': '28px',
                    'color': color,
                    'marginBottom': '10px'
                })
            ]),
            html.Div([
                html.P(title, style={
                    'color': COLORS['text_muted'],
                    'fontSize': '13px',
                    'margin': '0 0 8px 0',
                    'fontWeight': '500'
                }),
                html.H2(id=id, children=value, style={
                    'color': COLORS['text'],
                    'fontSize': '28px',
                    'fontWeight': '700',
                    'margin': '0 0 8px 0'
                }),
                html.P(change, style={
                    'color': COLORS['success'],
                    'fontSize': '12px',
                    'margin': '0',
                    'fontWeight': '500'
                })
            ])
        ])
    ], style=KPI_CARD_STYLE)

# ============================================================================
# CALLBACKS
# ============================================================================

@app.callback(
    [Output('revenue-card', 'children'),
     Output('transactions-card', 'children'),
     Output('avg-ticket-card', 'children'),
     Output('items-card', 'children'),
     Output('sales-trend-chart', 'figure'),
     Output('sales-by-hour-chart', 'figure'),
     Output('sales-by-category-chart', 'figure'),
     Output('sales-by-day-chart', 'figure'),
     Output('sales-by-location-chart', 'figure'),
     Output('top-products-chart', 'figure')],
    [Input('location-filter', 'value'),
     Input('month-filter', 'value')]
)
def update_dashboard(selected_location, selected_month):
    """Actualiza todos los componentes del dashboard basado en los filtros"""
    
    # Cargar datos
    df = load_data()
    
    # Aplicar filtros
    filtered_df = df.copy()
    if selected_location != 'Todas':
        filtered_df = filtered_df[filtered_df['store_location'] == selected_location]
    if selected_month != 'Todos':
        filtered_df = filtered_df[filtered_df['Month Name'] == selected_month]
    
    # Calcular métricas
    metrics = calculate_metrics(filtered_df)
    
    # KPIs
    revenue_text = f"${metrics['total_revenue']:,.2f}"
    transactions_text = f"{metrics['total_transactions']:,}"
    avg_ticket_text = f"${metrics['avg_ticket']:.2f}"
    items_text = f"{metrics['total_items']:,}"
    
    # Crear gráficos
    sales_trend_fig = create_sales_trend_chart(filtered_df)
    sales_hour_fig = create_sales_by_hour_chart(filtered_df)
    sales_category_fig = create_sales_by_category_chart(filtered_df)
    sales_day_fig = create_sales_by_day_chart(filtered_df)
    sales_location_fig = create_sales_by_location_chart(filtered_df)
    top_products_fig = create_top_products_chart(filtered_df)
    
    return (revenue_text, transactions_text, avg_ticket_text, items_text,
            sales_trend_fig, sales_hour_fig, sales_category_fig,
            sales_day_fig, sales_location_fig, top_products_fig)

# ============================================================================
# FUNCIONES PARA CREAR GRÁFICOS
# ============================================================================

def get_chart_layout(title=''):
    """Retorna el layout base para los gráficos"""
    return {
        'plot_bgcolor': COLORS['card'],
        'paper_bgcolor': COLORS['card'],
        'font': {'color': COLORS['text'], 'size': 12},
        'margin': {'l': 40, 'r': 20, 't': 10, 'b': 40},
        'xaxis': {
            'gridcolor': COLORS['border'],
            'showgrid': True,
            'zeroline': False
        },
        'yaxis': {
            'gridcolor': COLORS['border'],
            'showgrid': True,
            'zeroline': False
        },
        'hovermode': 'closest'
    }

def create_sales_trend_chart(df):
    """Crea el gráfico de tendencia de ventas"""
    data = get_sales_trend(df)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=data['Date'],
        y=data['Total'],
        mode='lines+markers',
        name='Ventas',
        line={'color': COLORS['primary'], 'width': 3},
        marker={'size': 6, 'color': COLORS['primary']},
        fill='tozeroy',
        fillcolor=f'rgba(59, 130, 246, 0.1)',
        hovertemplate='<b>%{x|%d/%m/%Y}</b><br>Ventas: $%{y:,.2f}<extra></extra>'
    ))
    
    fig.update_layout(get_chart_layout())
    fig.update_xaxes(title='Fecha')
    fig.update_yaxes(title='Ingresos ($)')
    
    return fig

def create_sales_by_hour_chart(df):
    """Crea el gráfico de ventas por hora"""
    data = get_sales_by_hour(df)
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=data['Hour'],
        y=data['Total'],
        marker={'color': COLORS['primary'], 'opacity': 0.8},
        hovertemplate='<b>Hora %{x}:00</b><br>Ventas: $%{y:,.2f}<extra></extra>'
    ))
    
    fig.update_layout(get_chart_layout())
    fig.update_xaxes(title='Hora del Día')
    fig.update_yaxes(title='Ingresos ($)')
    
    return fig

def create_sales_by_category_chart(df):
    """Crea el gráfico de ventas por categoría"""
    data = get_sales_by_category(df)
    
    colors_list = [COLORS['primary'], COLORS['success'], COLORS['warning'], 
                   COLORS['secondary'], COLORS['danger']]
    
    fig = go.Figure()
    fig.add_trace(go.Pie(
        labels=data['Category'],
        values=data['Total'],
        marker={'colors': colors_list},
        textposition='inside',
        textinfo='label+percent',
        hovertemplate='<b>%{label}</b><br>Ventas: $%{value:,.2f}<br>%{percent}<extra></extra>'
    ))
    
    layout = get_chart_layout()
    layout['showlegend'] = False
    fig.update_layout(layout)
    
    return fig

def create_sales_by_day_chart(df):
    """Crea el gráfico de ventas por día"""
    data = get_sales_by_day(df)
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=data['Day'],
        y=data['Total'],
        marker={'color': COLORS['success'], 'opacity': 0.8},
        hovertemplate='<b>%{x}</b><br>Ventas: $%{y:,.2f}<extra></extra>'
    ))
    
    fig.update_layout(get_chart_layout())
    fig.update_xaxes(title='Día de la Semana')
    fig.update_yaxes(title='Ingresos ($)')
    
    return fig

def create_sales_by_location_chart(df):
    """Crea el gráfico de ventas por ubicación"""
    data = get_sales_by_location(df)
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=data['Location'],
        y=data['Total'],
        marker={'color': COLORS['secondary'], 'opacity': 0.8},
        hovertemplate='<b>%{x}</b><br>Ventas: $%{y:,.2f}<extra></extra>'
    ))
    
    fig.update_layout(get_chart_layout())
    fig.update_xaxes(title='Ubicación')
    fig.update_yaxes(title='Ingresos ($)')
    
    return fig

def create_top_products_chart(df):
    """Crea el gráfico de productos más vendidos"""
    data = get_top_products(df)
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=data['Product'],
        x=data['Quantity'],
        orientation='h',
        marker={
            'color': data['Quantity'],
            'colorscale': [[0, COLORS['primary_light']], [1, COLORS['primary']]],
            'opacity': 0.8
        },
        hovertemplate='<b>%{y}</b><br>Cantidad: %{x}<br>Ingresos: $%{customdata:,.2f}<extra></extra>',
        customdata=data['Revenue']
    ))
    
    layout = get_chart_layout()
    layout['height'] = 400
    layout['margin'] = {'l': 200, 'r': 20, 't': 10, 'b': 40}
    fig.update_layout(layout)
    fig.update_xaxes(title='Cantidad Vendida')
    fig.update_yaxes(title='')
    
    return fig

# ============================================================================
# INICIALIZACIÓN
# ============================================================================

# Cargar datos iniciales
try:
    initial_df = load_data()
    app.layout = create_layout(initial_df)
    print("\n" + "="*60)
    print("✓ Dashboard iniciado correctamente")
    print("="*60)
    print(f"Total de registros: {len(initial_df):,}")
    print(f"Ubicaciones: {', '.join(initial_df['store_location'].unique())}")
    print(f"Período: {initial_df['Month Name'].unique()[0]}")
    print("="*60 + "\n")
except Exception as e:
    print(f"Error al inicializar el dashboard: {e}")
    app.layout = html.Div([
        html.H1("Error al cargar datos"),
        html.P(f"Detalles: {str(e)}")
    ])

# ============================================================================
# EJECUTAR SERVIDOR
# ============================================================================

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8050)
