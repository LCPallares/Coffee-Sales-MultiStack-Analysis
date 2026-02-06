# config.py
import flet as ft
from datetime import datetime

# Colores del tema
COLORS = {
    "primary": "#6F4E37",  # Café principal
    "secondary": "#C19A6B",  # Café claro
    "success": "#4CAF50",  # Verde
    "warning": "#FF9800",  # Naranja
    "danger": "#F44336",  # Rojo
    "info": "#2196F3",  # Azul
    "light": "#F5F5F5",  # Gris claro
    "dark": "#333333",  # Gris oscuro
    "bg": "#FAF3E0",  # Fondo beige claro
    "accent": "#8B4513",  # Café oscuro
}

# Configuración de la aplicación
APP_CONFIG = {
    "title": "Coffee Shop Analytics",
    "version": "1.0.0",
    "author": "Coffee Analytics Team",
    "data_file": "coffee_shop_sales.csv",
}

# Rutas de las páginas
PAGES = {
    "dashboard": "Dashboard",
    "sales": "Ventas",
    "products": "Productos", 
    "analytics": "Analytics",
    "stores": "Tiendas",
    "settings": "Configuración",
}

# Iconos para el menú
PAGE_ICONS = {
    "dashboard": ft.Icons.DASHBOARD,
    "sales": ft.Icons.SHOPPING_CART,
    "products": ft.Icons.COFFEE,
    "analytics": ft.Icons.BAR_CHART,
    "stores": ft.Icons.STORE,
    "settings": ft.Icons.SETTINGS,
}