# utils/helpers.py
import flet as ft
from datetime import datetime
from typing import List, Dict, Any

def format_currency(value: float) -> str:
    """Formatea un valor como moneda"""
    return f"${value:,.2f}"

def format_number(value: int) -> str:
    """Formatea un número con separadores de miles"""
    return f"{value:,}"

def create_data_table(columns: List[str], rows: List[List[Any]]) -> ft.DataTable:
    """Crea una tabla de datos"""
    return ft.DataTable(
        columns=[ft.DataColumn(ft.Text(col)) for col in columns],
        rows=[
            ft.DataRow(cells=[ft.DataCell(ft.Text(str(cell))) for cell in row])
            for row in rows
        ]
    )

def create_filter_row(on_filter_change) -> ft.Row:
    """Crea una fila de filtros"""
    return ft.Row([
        ft.TextField(
            label="Buscar...",
            prefix_icon=ft.Icons.SEARCH,
            on_change=on_filter_change,
            expand=True
        ),
        ft.Dropdown(
            label="Ordenar por",
            options=[
                ft.dropdown.Option("Fecha"),
                ft.dropdown.Option("Monto"),
                ft.dropdown.Option("Categoría"),
            ],
            value="Fecha",
            width=150
        ),
        ft.Dropdown(
            label="Período",
            options=[
                ft.dropdown.Option("Hoy"),
                ft.dropdown.Option("Últimos 7 días"),
                ft.dropdown.Option("Últimos 30 días"),
                ft.dropdown.Option("Todo"),
            ],
            value="Últimos 30 días",
            width=150
        ),
    ], spacing=10)