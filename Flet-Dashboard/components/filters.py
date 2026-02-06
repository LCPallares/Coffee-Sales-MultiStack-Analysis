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
            'year': 2023,
            'months': ['all'],  # ['all'] o [1, 2, 3, 4, 5, 6]
            'quarters': [],     # [] o ['Q1', 'Q2']
            'store': 'Todos',
            'category': 'Todos'
        }
        
        # Meses disponibles basados en los datos
        self.available_months = [
            {'name': 'Enero', 'number': 1, 'checkbox': None},
            {'name': 'Febrero', 'number': 2, 'checkbox': None},
            {'name': 'Marzo', 'number': 3, 'checkbox': None},
            {'name': 'Abril', 'number': 4, 'checkbox': None},
            {'name': 'Mayo', 'number': 5, 'checkbox': None},
            {'name': 'Junio', 'number': 6, 'checkbox': None}
        ]
    
    def build(self) -> ft.Container:
        """Construye el panel de filtros"""
        # Obtener opciones únicas
        stores = ['Todos'] + self.data_loader.get_unique_values('store_location')
        categories = ['Todos'] + self.data_loader.get_unique_values('product_category')
        
        # Crear checkboxes para meses
        for month in self.available_months:
            month['checkbox'] = ft.Checkbox(
                label=month['name'],
                value=False,
                on_change=lambda e, m=month: self._toggle_month(m, e.control.value)
            )
        
        # Crear controles de filtro
        year_dropdown = ft.Dropdown(
            label="Año",
            width=120,
            options=[
                ft.dropdown.Option("2023"),
            ],
            value="2023",
            on_change=lambda e: self._update_filter('year', int(e.control.value))
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
            content=ft.Column([
                # Primera fila de filtros principales
                ft.Row([
                    # Botón de filtros avanzados
                    ft.IconButton(
                        icon=ft.Icons.FILTER_LIST,
                        icon_color=COLORS["primary"],
                        tooltip="Filtros avanzados"
                    ),
                    
                    # Filtro por año
                    year_dropdown,
                    
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
                
                # Segunda fila - Filtros de meses y quarters
                ft.Row([
                    # Contenedor de meses
                    ft.Container(
                        content=ft.Column([
                            ft.Text("Meses:", size=14, weight=ft.FontWeight.BOLD),
                            ft.Row([
                                ft.Column([
                                    month['checkbox'] for month in self.available_months[:3]
                                ]),
                                ft.Column([
                                    month['checkbox'] for month in self.available_months[3:]
                                ])
                            ])
                        ]),
                        margin=ft.margin.only(right=20)
                    ),
                    
                    # Botones rápidos de quarters
                    ft.Container(
                        content=ft.Column([
                            ft.Text("Selección Rápida:", size=14, weight=ft.FontWeight.BOLD),
                            ft.Row([
                                ft.ElevatedButton(
                                    "Q1 2023",
                                    on_click=lambda e: self._select_quarter('Q1'),
                                    style=ft.ButtonStyle(
                                        bgcolor=COLORS["primary"],
                                        color=ft.Colors.WHITE
                                    )
                                ),
                                ft.ElevatedButton(
                                    "Q2 2023", 
                                    on_click=lambda e: self._select_quarter('Q2'),
                                    style=ft.ButtonStyle(
                                        bgcolor=COLORS["primary"],
                                        color=ft.Colors.WHITE
                                    )
                                ),
                                ft.ElevatedButton(
                                    "1er Semestre",
                                    on_click=lambda e: self._select_all_months(),
                                    style=ft.ButtonStyle(
                                        bgcolor=COLORS["success"],
                                        color=ft.Colors.WHITE
                                    )
                                )
                            ])
                        ]),
                        expand=True
                    )
                ])
            ]),
            padding=ft.padding.symmetric(vertical=10, horizontal=20),
            bgcolor=ft.Colors.WHITE,
            border_radius=10,
            margin=ft.margin.only(bottom=20)
        )
    
    def _toggle_month(self, month_data, is_checked):
        """Activa/desactiva un mes específico"""
        if is_checked:
            if 'all' in self.filters['months']:
                self.filters['months'] = [month_data['number']]
            else:
                self.filters['months'].append(month_data['number'])
        else:
            if month_data['number'] in self.filters['months']:
                self.filters['months'].remove(month_data['number'])
        
        # Si no hay meses seleccionados, volver a 'all'
        if not self.filters['months']:
            self.filters['months'] = ['all']
            # Resetear todos los checkboxes
            for month in self.available_months:
                month['checkbox'].value = False
        
        self.on_filter_change(self.filters)
    
    def _select_quarter(self, quarter):
        """Selecciona los meses de un quarter específico"""
        quarter_months = {
            'Q1': [1, 2, 3],  # Enero, Febrero, Marzo
            'Q2': [4, 5, 6]   # Abril, Mayo, Junio
        }
        
        months_to_select = quarter_months.get(quarter, [])
        
        # Limpiar selección actual
        self.filters['months'] = []
        for month in self.available_months:
            month['checkbox'].value = False
        
        # Seleccionar meses del quarter
        for month in self.available_months:
            if month['number'] in months_to_select:
                month['checkbox'].value = True
                self.filters['months'].append(month['number'])
        
        self.filters['quarters'] = [quarter]
        self.on_filter_change(self.filters)
    
    def _select_all_months(self):
        """Selecciona todos los meses disponibles"""
        self.filters['months'] = [month['number'] for month in self.available_months]
        self.filters['quarters'] = []
        
        for month in self.available_months:
            month['checkbox'].value = True
        
        self.on_filter_change(self.filters)
    
    def _update_filter(self, filter_name, value):
        """Actualiza un filtro específico"""
        self.filters[filter_name] = value
        self.on_filter_change(self.filters)
    
    def _clear_filters(self):
        """Limpia todos los filtros"""
        self.filters = {
            'year': 2023,
            'months': ['all'],
            'quarters': [],
            'store': 'Todos',
            'category': 'Todos'
        }
        
        # Resetear checkboxes de meses
        for month in self.available_months:
            month['checkbox'].value = False
        
        self.on_filter_change(self.filters)