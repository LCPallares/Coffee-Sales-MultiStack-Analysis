# pages/sales.py
import flet as ft
import pandas as pd
from config import COLORS
from components.cards import SalesChartCard

class SalesPage:
    def __init__(self, data_loader):
        self.data_loader = data_loader
    
    def build(self) -> ft.Container:
        """Construye la página de ventas"""
        # Obtener datos
        hourly_sales = self.data_loader.get_hourly_sales()
        store_performance = self.data_loader.get_store_performance()
        daily_sales = self.data_loader.get_daily_sales()
        
        # Preparar datos para gráficos
        hourly_data = hourly_sales['revenue'].tolist() if not hourly_sales.empty else []
        hourly_labels = [f"{h}:00" for h in hourly_sales['hour'].tolist()] if not hourly_sales.empty else []
        
        # Gráfico de ventas por hora
        hourly_chart = SalesChartCard.create(
            title="Ventas por Hora del Día",
            data=hourly_data,
            labels=hourly_labels
        )
        
        # Tabla de rendimiento de tiendas
        store_rows = []
        if not store_performance.empty:
            for _, store in store_performance.iterrows():
                store_rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(f"Tienda {int(store['store_id'])}")),
                            ft.DataCell(ft.Text(store['store_location'])),
                            ft.DataCell(ft.Text(f"{int(store['transaction_id']):,}")),
                            ft.DataCell(ft.Text(f"${store['revenue']:,.0f}")),
                            ft.DataCell(ft.Text(f"{int(store['transaction_qty']):,}")),
                            ft.DataCell(
                                ft.Container(
                                    content=ft.Text("Ver Detalles"),
                                    padding=5,
                                    bgcolor=COLORS["primary"],
                                    border_radius=5,
                                    on_click=lambda e: print("Ver detalles")
                                )
                            ),
                        ]
                    )
                )
        
        store_table = ft.Container(
            content=ft.Column([
                ft.Text("Rendimiento por Tienda", size=20, weight=ft.FontWeight.BOLD),
                ft.Divider(height=20),
                ft.DataTable(
                    columns=[
                        ft.DataColumn(ft.Text("ID Tienda")),
                        ft.DataColumn(ft.Text("Ubicación")),
                        ft.DataColumn(ft.Text("Transacciones")),
                        ft.DataColumn(ft.Text("Ingresos")),
                        ft.DataColumn(ft.Text("Cantidad Vendida")),
                        ft.DataColumn(ft.Text("Acciones")),
                    ],
                    rows=store_rows,
                )
            ]),
            padding=20,
            bgcolor=ft.Colors.WHITE,
            border_radius=15,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=10,
                color=ft.Colors.BLACK12,
                offset=ft.Offset(0, 2)
            )
        )
        
        # Métricas de ventas diarias
        if not daily_sales.empty:
            avg_daily = daily_sales['revenue'].mean()
            max_daily = daily_sales['revenue'].max()
            min_daily = daily_sales['revenue'].min()
        else:
            avg_daily = max_daily = min_daily = 0
        
        metrics_row = ft.Row([
            ft.Container(
                content=ft.Column([
                    ft.Text("Promedio Diario", size=14, color=ft.Colors.GREY),
                    ft.Text(f"${avg_daily:,.0f}", size=24, weight=ft.FontWeight.BOLD)
                ]),
                padding=20,
                bgcolor=ft.Colors.WHITE,
                border_radius=10,
                expand=True
            ),
            ft.Container(
                content=ft.Column([
                    ft.Text("Máximo Diario", size=14, color=ft.Colors.GREY),
                    ft.Text(f"${max_daily:,.0f}", size=24, weight=ft.FontWeight.BOLD)
                ]),
                padding=20,
                bgcolor=ft.Colors.WHITE,
                border_radius=10,
                expand=True
            ),
            ft.Container(
                content=ft.Column([
                    ft.Text("Mínimo Diario", size=14, color=ft.Colors.GREY),
                    ft.Text(f"${min_daily:,.0f}", size=24, weight=ft.FontWeight.BOLD)
                ]),
                padding=20,
                bgcolor=ft.Colors.WHITE,
                border_radius=10,
                expand=True
            ),
        ], spacing=20)
        
        # Contenido completo
        content = ft.Column([
            metrics_row,
            ft.Divider(height=30, color=ft.Colors.TRANSPARENT),
            hourly_chart,
            ft.Divider(height=30, color=ft.Colors.TRANSPARENT),
            store_table
        ])
        
        return ft.Container(
            content=content,
            padding=20,
            expand=True,
            bgcolor=COLORS["bg"]
        )