# components/filters.py
import flet as ft
from datetime import datetime, timedelta
from config import COLORS

class FilterPanel:
    def __init__(self, data_loader, on_filter_change):
        self.data_loader = data_loader
        self.on_filter_change = on_filter_change
        
        # Estado de filtros
        self.filters = {
            'period': 'last_30_days',
            'store': 'all',
            'category': 'all',
            'product_type': 'all'
        }
    
    def build(self) -> ft.Container:
        """Construye el panel de filtros"""
        # Obtener opciones únicas
        stores = ['Todos'] + self.data_loader.get_unique_values('store_location')
        categories = ['Todos'] + self.data_loader.get_unique_values('product_category')
        
        # Crear controles de filtro
        period_dropdown = ft.Dropdown(
            label="Período",
            width=150,
            options=[
                ft.dropdown.Option("Hoy"),
                ft.dropdown.Option("Últimos 7 días"),
                ft.dropdown.Option("Últimos 30 días"),
                ft.dropdown.Option("Últimos 90 días"),
                ft.dropdown.Option("Este mes"),
                ft.dropdown.Option("Mes anterior"),
                ft.dropdown.Option("Todo"),
            ],
            value="Últimos 30 días",
            on_change=lambda e: self._update_filter('period', e.control.value)
        )
        
        store_dropdown = ft.Dropdown(
            label="Tienda",
            width=150,
            options=[ft.dropdown.Option(store) for store in stores],
            value="Todos",
            on_change=lambda e: self._update_filter('store', e.control.value)
        )
        
        category_dropdown = ft.Dropdown(
            label="Categoría",
            width=150,
            options=[ft.dropdown.Option(cat) for cat in categories],
            value="Todos",
            on_change=lambda e: self._update_filter('category', e.control.value)
        )
        
        return ft.Container(
            content=ft.Row([
                # Botón de filtros avanzados
                ft.IconButton(
                    icon=ft.Icons.FILTER_LIST,
                    icon_color=COLORS["primary"],
                    tooltip="Filtros avanzados"
                ),
                
                # Filtro por período
                period_dropdown,
                
                # Filtro por tienda
                store_dropdown,
                
                # Filtro por categoría
                category_dropdown,
                
                # Botón para limpiar filtros
                ft.ElevatedButton(
                    "Limpiar Filtros",
                    icon=ft.Icons.CLEAR_ALL,
                    on_click=lambda e: self._clear_filters(),
                    style=ft.ButtonStyle(
                        bgcolor=ft.Colors.GREY_200,
                        color=ft.Colors.BLACK
                    )
                ),
                
                # Espaciador
                ft.Container(expand=True),
                
                # Botón de actualizar
                ft.IconButton(
                    icon=ft.Icons.REFRESH,
                    icon_color=COLORS["primary"],
                    tooltip="Actualizar datos"
                )
            ], alignment=ft.MainAxisAlignment.START),
            padding=ft.padding.symmetric(vertical=10, horizontal=20),
            bgcolor=ft.Colors.WHITE,
            border_radius=10,
            margin=ft.margin.only(bottom=20)
        )
    
    def _update_filter(self, filter_name, value):
        """Actualiza un filtro específico"""
        self.filters[filter_name] = value
        self.on_filter_change(self.filters)
    
    def _clear_filters(self):
        """Limpia todos los filtros"""
        self.filters = {
            'period': 'last_30_days',
            'store': 'all',
            'category': 'all',
            'product_type': 'all'
        }
        self.on_filter_change(self.filters)