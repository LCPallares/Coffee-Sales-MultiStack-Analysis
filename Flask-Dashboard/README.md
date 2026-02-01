# Coffee Shop Sales Dashboard - Flask

Dashboard interactivo para análisis de ventas de una cafetería, convertido de Streamlit a Flask.

## 📋 Características

- **Overview**: Visualización general de ventas, KPIs y análisis por categorías
- **Monthly Sales**: Análisis detallado mensual con comparativas
- **Shopper Behavior**: Patrones de comportamiento del consumidor
- **Advanced Analytics**: Análisis avanzados de tendencias temporales

## 🛠️ Estructura del Proyecto

```
flask_coffee_dashboard/
├── app.py                      # Aplicación principal Flask
├── requirements.txt            # Dependencias del proyecto
├── data/
│   └── coffee_shop_sales.csv  # Dataset (debes colocarlo aquí)
├── static/
│   └── css/
│       └── style.css          # Estilos personalizados
└── templates/
    ├── base.html              # Template base
    ├── overview.html          # Página de Overview
    ├── monthly.html           # Página de Monthly Sales
    ├── behavior.html          # Página de Shopper Behavior
    └── advanced.html          # Página de Advanced Analytics
```

## 🚀 Instalación y Ejecución

### 1. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 2. Colocar el archivo de datos

Asegúrate de colocar tu archivo `coffee_shop_sales.csv` en la carpeta `data/`:

```
flask_coffee_dashboard/
└── data/
    └── coffee_shop_sales.csv
```

### 3. Ejecutar la aplicación

```bash
python app.py
```

La aplicación estará disponible en: `http://localhost:5000`

## 📊 Rutas Disponibles

- `/` o `/overview` - Página principal con overview general
- `/monthly` - Análisis mensual detallado
- `/behavior` - Comportamiento del consumidor
- `/advanced` - Análisis avanzados

Todas las rutas aceptan el parámetro `month` para filtrar por mes:
- Ejemplo: `/overview?month=January`
- Ejemplo: `/monthly?month=March`

## 🎨 Características del Dashboard

### Overview
- KPIs principales (Ventas, Cantidad, Transacciones)
- Ventas por categoría (gráfico de barras)
- Distribución por tienda (gráfico de pastel)
- Tendencia mensual global
- Tabla resumen ejecutiva

### Monthly Sales
- KPIs con comparativa vs mes anterior
- Ventas diarias del mes seleccionado
- Comparativa de categorías mes actual vs anterior
- Tabla resumen del mes

### Shopper Behavior
- Mapa de calor de tráfico (Horas vs Días)
- Totales por día de la semana
- Análisis de precio vs volumen
- Matriz estratégica de categorías
- Top 10 productos

### Advanced Analytics
- Distribución temporal de ventas por tienda
- Análisis de tendencia diaria con doble eje
- Evolución de ventas y ticket promedio

## 🎨 Paleta de Colores

- **Coffee Dark**: #3d2b1f
- **Coffee Medium**: #6f4e37
- **Coffee Light**: #c3a689
- **Cream**: #fdf5e6

## 📝 Diferencias con Streamlit

1. **Navegación**: En lugar de sidebar con radio buttons, ahora tienes un menú lateral fijo con enlaces
2. **Filtros**: El selector de mes está en el sidebar y se aplica a todas las páginas
3. **Interactividad**: Los gráficos Plotly mantienen toda su interactividad
4. **Rutas**: Cada página de Streamlit es ahora una ruta Flask independiente
5. **Performance**: Los datos se cargan una sola vez al iniciar la aplicación

## 🔧 Personalización

### Cambiar puerto o host

Edita la última línea en `app.py`:

```python
app.run(debug=True, host='0.0.0.0', port=5000)
```

### Modificar estilos

Los estilos CSS están en `static/css/style.css`. Puedes modificar las variables CSS:

```css
:root {
    --coffee-dark: #3d2b1f;
    --coffee-medium: #6f4e37;
    --coffee-light: #c3a689;
    --cream: #fdf5e6;
}
```

### Agregar nuevas páginas

1. Crea una nueva ruta en `app.py`
2. Crea el template correspondiente en `templates/`
3. Agrega el enlace en `base.html`

## 📦 Dependencias

- **Flask 3.0.0**: Framework web
- **Pandas 2.1.4**: Procesamiento de datos
- **Plotly 5.18.0**: Visualizaciones interactivas

## 🐛 Troubleshooting

### Error: No module named 'flask'
```bash
pip install Flask
```

### Error: FileNotFoundError para el CSV
Asegúrate de que el archivo `coffee_shop_sales.csv` esté en la carpeta `data/`

### Los gráficos no se muestran
Verifica que la conexión a Internet esté activa (Plotly se carga desde CDN)

## 📄 Licencia

Este proyecto es una conversión del dashboard de Streamlit a Flask para propósitos educativos.
