# 📚 Ejemplos de Extensión del Dashboard

Este archivo contiene ejemplos prácticos de cómo agregar nuevas funcionalidades al dashboard.

## 🎯 Ejemplo 1: Agregar Gráfico de Ventas por Tamaño

### Paso 1: Agregar función en `components/charts.py`

```python
def create_size_distribution(df):
    """
    Create a donut chart showing revenue distribution by product size
    """
    
    size_sales = df.groupby('Size')['Total_Bill'].sum().reset_index()
    size_sales = size_sales.sort_values('Total_Bill', ascending=False)
    
    fig = go.Figure(
        data=[
            go.Pie(
                labels=size_sales['Size'],
                values=size_sales['Total_Bill'],
                hole=0.5,
                marker=dict(
                    colors=['#8B4513', '#C09F76', '#D4B896'],
                    line=dict(color='white', width=2)
                ),
                textposition='auto',
                textinfo='label+percent',
                hovertemplate='<b>%{label}</b><br>Revenue: $%{value:,.2f}<br>%{percent}<extra></extra>'
            )
        ]
    )
    
    fig = style_chart(fig, title="Revenue by Size", height=400)
    
    return dcc.Graph(figure=fig, config={'displayModeBar': False})
```

### Paso 2: Importar en `app.py`

```python
from components.charts import (
    create_sales_trend,
    create_category_distribution,
    create_hourly_heatmap,
    create_top_products,
    create_store_comparison,
    create_weekday_analysis,
    create_size_distribution  # ← NUEVO
)
```

### Paso 3: Agregar al layout

```python
# En la sección de Grid, agregar:
dmc.GridCol(
    span={"base": 12, "md": 6},
    children=dmc.Paper(
        shadow="sm",
        p="md",
        withBorder=True,
        children=html.Div(id="size-chart")
    )
),
```

### Paso 4: Actualizar callback

```python
@callback(
    [
        Output("kpi-cards", "children"),
        Output("sales-trend-chart", "children"),
        Output("category-distribution-chart", "children"),
        Output("top-products-chart", "children"),
        Output("heatmap-chart", "children"),
        Output("store-chart", "children"),
        Output("weekday-chart", "children"),
        Output("size-chart", "children")  # ← NUEVO
    ],
    # ... inputs ...
)
def update_dashboard(date_range, stores, categories, products):
    # ... código existente ...
    
    return (
        create_kpi_cards(filtered_df),
        create_sales_trend(filtered_df),
        create_category_distribution(filtered_df),
        create_top_products(filtered_df),
        create_hourly_heatmap(filtered_df),
        create_store_comparison(filtered_df),
        create_weekday_analysis(filtered_df),
        create_size_distribution(filtered_df)  # ← NUEVO
    )
```

## 📊 Ejemplo 2: Agregar Métrica de Ticket Promedio por Hora

### En `components/kpi_cards.py`

```python
def create_kpi_cards(df):
    metrics = calculate_metrics(df)
    
    # Calcular ticket promedio por hora
    hourly_avg = df.groupby('Hour')['Total_Bill'].mean()
    peak_hour = hourly_avg.idxmax()
    peak_value = hourly_avg.max()
    
    cards = [
        # ... tarjetas existentes ...
        {
            "title": "Peak Hour Average",
            "value": f"${peak_value:.2f}",
            "icon": "tabler:clock-hour-4",
            "color": "grape",
            "trend": None,
            "trend_label": f"at {peak_hour}:00"
        }
    ]
    
    # ... resto del código ...
```

## 🔍 Ejemplo 3: Agregar Filtro de Rango de Precio

### En `components/filters.py`

```python
# Obtener rango de precios
min_price = df['unit_price'].min()
max_price = df['unit_price'].max()

# Agregar al Grid:
dmc.GridCol(
    span={"base": 12, "sm": 6, "md": 3},
    children=dmc.Stack(
        gap="xs",
        children=[
            dmc.Group(
                gap="xs",
                children=[
                    DashIconify(icon="tabler:cash", width=18, color="#8B4513"),
                    dmc.Text("Price Range", size="sm", fw=600)
                ]
            ),
            dmc.RangeSlider(
                id="price-filter",
                min=min_price,
                max=max_price,
                value=[min_price, max_price],
                marks=[
                    {"value": min_price, "label": f"${min_price}"},
                    {"value": max_price, "label": f"${max_price}"}
                ],
                step=0.5
            )
        ]
    )
)
```

### Actualizar callback en `app.py`

```python
@callback(
    [Output(...)],
    [
        Input("date-range", "value"),
        Input("store-filter", "value"),
        Input("category-filter", "value"),
        Input("product-filter", "value"),
        Input("price-filter", "value")  # ← NUEVO
    ]
)
def update_dashboard(date_range, stores, categories, products, price_range):
    filtered_df = df.copy()
    
    # ... filtros existentes ...
    
    # Filtro de precio
    if price_range:
        filtered_df = filtered_df[
            (filtered_df['unit_price'] >= price_range[0]) &
            (filtered_df['unit_price'] <= price_range[1])
        ]
    
    # ... resto del código ...
```

## 📈 Ejemplo 4: Agregar Gráfico de Comparación Mensual

```python
def create_monthly_comparison(df):
    """
    Create a grouped bar chart comparing metrics across months
    """
    
    monthly = df.groupby('Month Name').agg({
        'Total_Bill': 'sum',
        'transaction_id': 'count',
        'transaction_qty': 'sum'
    }).reset_index()
    
    # Orden correcto de meses
    month_order = ['January', 'February', 'March', 'April', 'May', 'June',
                   'July', 'August', 'September', 'October', 'November', 'December']
    monthly['Month Name'] = pd.Categorical(
        monthly['Month Name'],
        categories=month_order,
        ordered=True
    )
    monthly = monthly.sort_values('Month Name')
    
    fig = go.Figure()
    
    # Revenue bars
    fig.add_trace(
        go.Bar(
            name='Revenue',
            x=monthly['Month Name'],
            y=monthly['Total_Bill'],
            marker_color=CHART_COLORS['primary'],
            yaxis='y',
            hovertemplate='<b>%{x}</b><br>Revenue: $%{y:,.2f}<extra></extra>'
        )
    )
    
    # Transactions bars
    fig.add_trace(
        go.Bar(
            name='Transactions',
            x=monthly['Month Name'],
            y=monthly['transaction_id'],
            marker_color=CHART_COLORS['secondary'],
            yaxis='y2',
            hovertemplate='<b>%{x}</b><br>Transactions: %{y}<extra></extra>'
        )
    )
    
    fig.update_layout(
        barmode='group',
        yaxis=dict(
            title='Revenue ($)',
            titlefont=dict(color=CHART_COLORS['primary'])
        ),
        yaxis2=dict(
            title='Transactions',
            overlaying='y',
            side='right',
            titlefont=dict(color=CHART_COLORS['secondary'])
        ),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    fig = style_chart(fig, title="Monthly Performance Comparison", height=400)
    
    return dcc.Graph(figure=fig, config={'displayModeBar': False})
```

## 🎨 Ejemplo 5: Personalizar Colores del Tema

### En `utils/theme.py`

```python
# Tema personalizado "Espresso Dark"
ESPRESSO_THEME = {
    "colorScheme": "dark",
    "primaryColor": "orange",
    "colors": {
        "dark": [
            "#C1C2C5",
            "#A6A7AB",
            "#909296",
            "#5C5F66",
            "#373A40",
            "#2C2E33",
            "#25262B",
            "#1A1B1E",
            "#141517",
            "#101113"
        ],
        "orange": [
            "#FFF4E6",
            "#FFE8CC",
            "#FFD8A8",
            "#FFC078",
            "#FFA94D",
            "#FF922B",  # Primary
            "#FD7E14",
            "#F76707",
            "#E8590C",
            "#D9480F"
        ]
    }
}

# Colores para gráficos modo oscuro
DARK_CHART_COLORS = {
    "primary": "#FF922B",
    "secondary": "#FFA94D",
    "accent": "#FFD8A8",
    "background": "#1A1B1E",
    "text": "#C1C2C5"
}
```

## 💡 Ejemplo 6: Agregar Tabla Interactiva con DataTable

```python
def create_sales_table(df, n=50):
    """
    Create an interactive data table showing recent transactions
    """
    
    # Seleccionar columnas importantes
    table_df = df.nlargest(n, 'transaction_date')[
        ['transaction_date', 'store_location', 'product_detail', 
         'transaction_qty', 'unit_price', 'Total_Bill']
    ].copy()
    
    # Formatear fecha
    table_df['transaction_date'] = table_df['transaction_date'].dt.strftime('%Y-%m-%d')
    
    return dmc.Paper(
        shadow="sm",
        p="md",
        withBorder=True,
        children=[
            dmc.Title("Recent Transactions", order=4, mb="md"),
            dmc.Table(
                striped=True,
                highlightOnHover=True,
                withBorder=True,
                data={
                    "head": ["Date", "Store", "Product", "Qty", "Price", "Total"],
                    "body": table_df.values.tolist()
                }
            )
        ]
    )
```

## 🔔 Ejemplo 7: Agregar Sistema de Notificaciones

```python
# En app.py, agregar al layout:
html.Div(id="notification-container"),

# Crear callback para notificaciones
@callback(
    Output("notification-container", "children"),
    Input("kpi-cards", "children")
)
def check_alerts(kpi_data):
    # Ejemplo: alertar si las ventas caen más del 10%
    notifications = []
    
    if metrics['revenue_growth'] < -10:
        notifications.append(
            dmc.Notification(
                title="⚠️ Sales Alert",
                message="Revenue has decreased by more than 10%",
                color="red",
                action="show"
            )
        )
    
    return notifications
```

## 📱 Ejemplo 8: Agregar Tabs para Múltiples Vistas

```python
# Envolver el contenido en Tabs
dmc.Tabs(
    value="overview",
    children=[
        dmc.TabsList([
            dmc.TabsTab("Overview", value="overview"),
            dmc.TabsTab("Products", value="products"),
            dmc.TabsTab("Stores", value="stores"),
            dmc.TabsTab("Time Analysis", value="time")
        ]),
        
        dmc.TabsPanel(
            value="overview",
            children=[
                # KPIs y gráficos principales
            ]
        ),
        
        dmc.TabsPanel(
            value="products",
            children=[
                # Análisis de productos
            ]
        ),
        
        # ... más panels
    ]
)
```

## 🎓 Tips Adicionales

### Optimización de Performance
```python
# Usar cache para datos que no cambian frecuentemente
from functools import lru_cache

@lru_cache(maxsize=32)
def get_filtered_data(date_str, stores_tuple, categories_tuple):
    # ... filtrar datos ...
    return filtered_df
```

### Agregar Loading States
```python
dcc.Loading(
    id="loading",
    type="default",
    children=html.Div(id="content")
)
```

### Exportar Datos
```python
dmc.Button(
    "Export to Excel",
    leftSection=DashIconify(icon="tabler:download"),
    onclick="window.open('/download/excel')"
)
```

---

Estos ejemplos te dan una base sólida para extender el dashboard según tus necesidades específicas. ¡Experimenta y personaliza!
