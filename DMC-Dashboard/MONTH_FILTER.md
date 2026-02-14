# 📅 Filtro de Meses - Documentación

## Nuevo Feature: Filtro por Meses

Se ha agregado un nuevo filtro que permite filtrar los datos por meses específicos, complementando el filtro de rango de fechas existente.

## 🎯 Ubicación

El filtro de meses se encuentra en la barra de filtros, entre el **Date Range** y el **Store Location**.

## 🔧 Características

- **Multi-selección**: Puedes seleccionar uno o varios meses
- **Ordenado**: Los meses aparecen en orden cronológico (Enero a Diciembre)
- **Búsqueda**: Campo searchable para encontrar meses rápidamente
- **Clearable**: Botón X para limpiar la selección
- **Icono**: Usa el icono `tabler:calendar-stats` para mejor UX

## 💡 Cómo Funciona

### 1. **Interacción con Date Range**

El filtro de meses trabaja en conjunto con el filtro de rango de fechas:

```
Ejemplo 1: 
- Date Range: 1 Enero 2023 - 31 Diciembre 2023
- Month Filter: Junio, Julio
- Resultado: Solo muestra datos de Junio y Julio de 2023

Ejemplo 2:
- Date Range: 1 Junio 2023 - 31 Agosto 2023  
- Month Filter: (vacío)
- Resultado: Muestra todos los días entre Junio y Agosto

Ejemplo 3:
- Date Range: 1 Enero 2023 - 31 Diciembre 2023
- Month Filter: Diciembre
- Resultado: Solo muestra datos de Diciembre 2023
```

### 2. **Filtrado en el Backend**

El filtro se implementa en el callback principal en `app.py`:

```python
@callback(
    [...],
    [
        Input("date-range", "value"),
        Input("month-filter", "value"),  # ← NUEVO
        Input("store-filter", "value"),
        Input("category-filter", "value"),
        Input("product-filter", "value")
    ]
)
def update_dashboard(date_range, months, stores, categories, products):
    filtered_df = df.copy()
    
    # ... filtro de date range ...
    
    # Filtro de meses
    if months:
        filtered_df = filtered_df[filtered_df['Month Name'].isin(months)]
    
    # ... otros filtros ...
```

### 3. **Obtención de Meses Únicos**

Los meses disponibles se extraen del dataset y se ordenan correctamente:

```python
# En components/filters.py
months_in_data = sorted(
    df['Month Name'].unique().tolist(), 
    key=lambda x: ['January', 'February', 'March', 'April', 'May', 'June',
                  'July', 'August', 'September', 'October', 'November', 'December'].index(x)
)
```

## 📊 Casos de Uso

### Análisis Estacional
```
Selecciona: Diciembre, Enero, Febrero
Objetivo: Analizar ventas en temporada de invierno
```

### Comparación Trimestral
```
Q1: Enero, Febrero, Marzo
Q2: Abril, Mayo, Junio
Q3: Julio, Agosto, Septiembre
Q4: Octubre, Noviembre, Diciembre
```

### Análisis de Temporada Alta
```
Selecciona: Junio, Julio, Agosto (verano)
Comparar con: Diciembre, Enero (invierno)
```

### Planificación de Inventario
```
Selecciona: Mes actual + próximos 2 meses
Analiza tendencias para planificar stock
```

## 🎨 Personalización

### Cambiar el Placeholder

```python
dmc.MultiSelect(
    id="month-filter",
    placeholder="Selecciona meses...",  # ← Cambiar aquí
    # ...
)
```

### Hacer Single-Select en vez de Multi

```python
dmc.Select(  # ← Cambiar a Select
    id="month-filter",
    data=months_in_data,
    placeholder="Selecciona un mes",
    # ...
)

# Y en el callback:
if months:  # Ahora es un string, no una lista
    filtered_df = filtered_df[filtered_df['Month Name'] == months]
```

### Agregar Mes por Defecto

```python
dmc.MultiSelect(
    id="month-filter",
    value=["June"],  # ← Mes pre-seleccionado
    # ...
)
```

## 🔄 Integración con Otros Filtros

El filtro de meses respeta todas las demás selecciones:

```python
Filtros activos:
✓ Meses: Junio, Julio
✓ Store: Astoria  
✓ Category: Coffee
✓ Product: Latte

Resultado: 
Solo transacciones que cumplan TODAS las condiciones
```

## 🐛 Troubleshooting

### Problema: No aparecen meses en el dropdown
**Solución**: Verifica que la columna 'Month Name' existe en tu CSV

### Problema: Meses en orden incorrecto
**Solución**: Revisa la función de sorting en `filters.py`

### Problema: El filtro no actualiza los gráficos
**Solución**: Verifica que el Input esté conectado al callback en `app.py`

## 📈 Próximas Mejoras

Ideas para extender el filtro de meses:

1. **Agrupación por Trimestre**: Botones quick-select para Q1, Q2, Q3, Q4
2. **Selector de Año**: Combinar con selector de año específico
3. **Comparación Año vs Año**: Seleccionar mismo mes de diferentes años
4. **Presets**: Botones como "Últimos 3 meses", "Año hasta la fecha", etc.

### Ejemplo: Quick Select Trimestral

```python
dmc.Group(
    gap="xs",
    children=[
        dmc.Button("Q1", size="xs", variant="light", 
                  id={"type": "quarter-btn", "index": "Q1"}),
        dmc.Button("Q2", size="xs", variant="light",
                  id={"type": "quarter-btn", "index": "Q2"}),
        dmc.Button("Q3", size="xs", variant="light",
                  id={"type": "quarter-btn", "index": "Q3"}),
        dmc.Button("Q4", size="xs", variant="light",
                  id={"type": "quarter-btn", "index": "Q4"}),
    ]
)

# Callback pattern matching
@callback(
    Output("month-filter", "value"),
    Input({"type": "quarter-btn", "index": ALL}, "n_clicks"),
    prevent_initial_call=True
)
def select_quarter(n_clicks):
    if not any(n_clicks):
        return dash.no_update
    
    ctx = dash.callback_context
    button_id = json.loads(ctx.triggered[0]['prop_id'].split('.')[0])
    
    quarters = {
        "Q1": ["January", "February", "March"],
        "Q2": ["April", "May", "June"],
        "Q3": ["July", "August", "September"],
        "Q4": ["October", "November", "December"]
    }
    
    return quarters[button_id["index"]]
```

---

## ✅ Checklist de Implementación

- [x] Agregar filtro al componente `filters.py`
- [x] Actualizar callback en `app.py` con nuevo Input
- [x] Agregar lógica de filtrado en la función `update_dashboard`
- [x] Ordenar meses cronológicamente
- [x] Probar interacción con otros filtros
- [x] Documentar el feature

¡El filtro de meses está completamente implementado y listo para usar! 🎉
