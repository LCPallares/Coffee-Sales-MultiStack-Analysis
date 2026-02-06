# pages/dashboard.py
import flet as ft
from config import COLORS
from components.cards import MetricCard, SalesChartCard, CategoryCard, RecentTransactionsCard

class DashboardPage:
    def __init__(self, data_loader):
        self.data_loader = data_loader
    
    def build(self) -> ft.Container:
        """Construye la página del dashboard"""
        # Obtener datos
        stats = self.data_loader.get_summary_stats()
        daily_sales = self.data_loader.get_daily_sales()
        category_sales = self.data_loader.get_category_sales()
        recent_transactions = self.data_loader.get_recent_transactions(5)
        
        # Preparar datos para gráficos
        last_7_days_data = daily_sales['revenue'].tail(7).tolist() if not daily_sales.empty else [0]*7
        last_7_days_labels = daily_sales['transaction_date'].dt.strftime('%d/%m').tail(7).tolist() if not daily_sales.empty else ['']*7
        
        # Tarjetas de métricas
        metric_cards = ft.Row([
            MetricCard.create(
                title="Ingresos Totales",
                value=f"${stats.get('total_revenue', 0):,.0f}",
                change=12.5,
                icon=ft.Icon(ft.Icons.ATTACH_MONEY, color=COLORS["primary"]),
                color=COLORS["primary"]
            ),
            MetricCard.create(
                title="Transacciones",
                value=f"{stats.get('total_transactions', 0):,}",
                change=8.2,
                icon=ft.Icon(ft.Icons.RECEIPT, color=COLORS["success"]),
                color=COLORS["success"]
            ),
            MetricCard.create(
                title="Valor Promedio",
                value=f"${stats.get('avg_transaction_value', 0):.2f}",
                change=-3.1,
                icon=ft.Icon(ft.Icons.TRENDING_UP, color=COLORS["warning"]),
                color=COLORS["warning"]
            ),
            MetricCard.create(
                title="Productos Únicos",
                value=f"{stats.get('unique_products', 0):,}",
                change=15.4,
                icon=ft.Icon(ft.Icons.COFFEE, color=COLORS["info"]),
                color=COLORS["info"]
            ),
        ], spacing=20)
        
        # Gráficos y tablas
        content = ft.Column([
            metric_cards,
            ft.Divider(height=30, color=ft.Colors.TRANSPARENT),
            ft.Row([
                SalesChartCard.create(
                    title="Ventas Últimos 7 Días",
                    data=last_7_days_data,
                    labels=last_7_days_labels
                ),
                CategoryCard.create(
                    title="Ventas por Categoría",
                    categories=category_sales['product_category'].tolist() if not category_sales.empty else [],
                    values=category_sales['revenue'].tolist() if not category_sales.empty else [],
                    colors=[COLORS["primary"], COLORS["secondary"], COLORS["success"], 
                           COLORS["warning"], COLORS["info"]]
                ),
            ], spacing=20),
            ft.Divider(height=30, color=ft.Colors.TRANSPARENT),
            RecentTransactionsCard.create(
                transactions=recent_transactions.to_dict('records') if not recent_transactions.empty else []
            )
        ])
        
        return ft.Container(
            content=content,
            padding=20,
            expand=True,
            bgcolor=COLORS["bg"]
        )