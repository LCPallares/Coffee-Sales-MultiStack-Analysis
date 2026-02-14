# ☕ Coffee Shop Sales Dashboard

Un dashboard profesional, escalable y modular construido con **Dash** y **Dash Mantine Components** para analizar ventas de una cafetería.

## 🎨 Características

- **Diseño Moderno**: Interfaz elegante con temática de café, usando tipografías distintivas (Playfair Display + Space Mono)
- **Arquitectura Modular**: Componentes separados y reutilizables para fácil escalabilidad
- **Filtros Interactivos**: Filtrado por fecha, tienda, categoría y producto
- **KPIs Dinámicos**: Métricas clave con indicadores de tendencia
- **Visualizaciones Múltiples**:
  - Tendencia de ventas temporal (dual-axis)
  - Distribución por categoría (pie chart)
  - Top productos por revenue (bar chart horizontal)
  - Heatmap de ventas por hora y día
  - Comparación entre tiendas
  - Análisis por día de la semana
- **100% Responsive**: Se adapta a cualquier dispositivo

## 📁 Estructura del Proyecto

```
coffee-dashboard/
├── app.py                      # Aplicación principal
├── requirements.txt            # Dependencias
├── coffee_shop_sales.csv       # Datos de ejemplo
├── components/                 # Componentes modulares
│   ├── __init__.py
│   ├── filters.py             # Controles de filtrado
│   ├── kpi_cards.py           # Tarjetas de KPIs
│   └── charts.py              # Todos los gráficos
└── utils/                      # Utilidades
    ├── __init__.py
    ├── data_loader.py         # Carga y preparación de datos
    └── theme.py               # Configuración de tema y estilos
```

## 🚀 Instalación y Uso

### 1. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 2. Ejecutar la aplicación

```bash
python app.py
```

### 3. Abrir en el navegador

Navega a: `http://localhost:8050`

## 📊 Agregar Nuevas Métricas y Gráficos

La arquitectura modular facilita agregar nuevas funcionalidades:

### Agregar un nuevo KPI

Edita `components/kpi_cards.py`:

```python
def create_kpi_cards(df):
    # ...existing code...
    
    # Agregar nueva tarjeta
    cards.append({
        "title": "Nueva Métrica",
        "value": f"${df['nueva_columna'].sum():,.2f}",
        "icon": "tabler:icon-name",
        "color": "teal",
        "trend": calculate_trend(df),
        "trend_label": "descripción"
    })
```

### Agregar un nuevo gráfico

1. **Crear función en `components/charts.py`**:

```python
def create_nuevo_grafico(df):
    """
    Descripción del nuevo gráfico
    """
    # Preparar datos
    data = df.groupby('columna')['valor'].sum()
    
    # Crear figura
    fig = go.Figure(
        data=[
            go.Bar(x=data.index, y=data.values)
        ]
    )
    
    # Aplicar estilo
    fig = style_chart(fig, title="Mi Nuevo Gráfico", height=400)
    
    return dcc.Graph(figure=fig, config={'displayModeBar': False})
```

2. **Importar en `app.py`**:

```python
from components.charts import (
    # ...existing imports...
    create_nuevo_grafico  # ← Agregar aquí
)
```

3. **Agregar al layout en `app.py`**:

```python
# En la sección de Grid, agregar:
dmc.GridCol(
    span={"base": 12, "md": 6},
    children=dmc.Paper(
        shadow="sm",
        p="md",
        withBorder=True,
        children=html.Div(id="nuevo-grafico-chart")
    )
)
```

4. **Actualizar callback en `app.py`**:

```python
@callback(
    [
        # ...existing outputs...
        Output("nuevo-grafico-chart", "children")  # ← Agregar
    ],
    # ...inputs...
)
def update_dashboard(...):
    # ...existing code...
    
    return (
        # ...existing returns...
        create_nuevo_grafico(filtered_df)  # ← Agregar
    )
```

### Agregar nuevos filtros

Edita `components/filters.py` y agrega el nuevo control en el Grid:

```python
dmc.GridCol(
    span={"base": 12, "sm": 6, "md": 3},
    children=dmc.Stack(
        gap="xs",
        children=[
            dmc.Group(
                gap="xs",
                children=[
                    DashIconify(icon="tabler:icon", width=18, color="#8B4513"),
                    dmc.Text("Nuevo Filtro", size="sm", fw=600)
                ]
            ),
            dmc.Select(
                id="nuevo-filtro",
                data=options,
                placeholder="Seleccionar..."
            )
        ]
    )
)
```

## 🎨 Personalizar Tema

Edita `utils/theme.py` para cambiar colores, fuentes y estilos:

```python
CHART_COLORS = {
    "primary": "#TU_COLOR",
    # ...
}

# Cambiar fuentes
"fontFamily": "'Tu-Fuente', sans-serif",
"headings": {
    "fontFamily": "'Tu-Fuente-Heading', serif"
}
```

## 🔧 Funciones Útiles en `utils/data_loader.py`

- `load_and_prepare_data(filepath)`: Carga y prepara los datos
- `calculate_metrics(df)`: Calcula métricas clave del negocio
- `get_top_products(df, n)`: Obtiene top N productos
- `get_category_summary(df)`: Resume ventas por categoría
- `classify_time_period(hour)`: Clasifica horas en períodos del día

## 📝 Formato de Datos

El CSV debe tener las siguientes columnas:

```
transaction_id, transaction_date, transaction_time, store_id, store_location,
product_id, transaction_qty, unit_price, Total_Bill, product_category,
product_type, product_detail, Size, Month Name, Day Name, Hour, Month, Day of Week
```

## 🎯 Próximas Mejoras Sugeridas

1. **Exportar a PDF/Excel**: Agregar botones para exportar reportes
2. **Filtros Avanzados**: Agregar filtro por rango de precios, tamaño, etc.
3. **Comparación Temporal**: Comparar períodos (mes actual vs anterior)
4. **Predicciones**: Agregar forecasting con modelos de ML
5. **Alertas**: Notificaciones cuando las métricas superen umbrales
6. **Drill-down**: Click en gráficos para ver detalles
7. **Dashboard por Usuario**: Múltiples dashboards personalizados

## 🛠️ Tecnologías Utilizadas

- **Dash 2.17.1**: Framework web de Python
- **Dash Mantine Components 0.14.4**: Componentes UI modernos
- **Plotly 5.20.0**: Gráficos interactivos
- **Pandas 2.2.1**: Manipulación de datos
- **Dash Iconify**: Iconos

## 📄 Licencia

Este proyecto es de código abierto y está disponible para uso personal y comercial.

## 👨‍💻 Autor

Creado con ☕ y 💻

---

**¿Preguntas o sugerencias?** ¡Abre un issue o contribuye al proyecto!
