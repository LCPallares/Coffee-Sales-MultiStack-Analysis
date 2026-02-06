# components/cards.py
import flet as ft
from config import COLORS

class MetricCard:
    @staticmethod
    def create(title: str, value: str, change: float, icon: ft.Icon, color: str) -> ft.Container:
        """Crea una tarjeta de métrica"""
        change_color = COLORS["success"] if change >= 0 else COLORS["danger"]
        change_icon = ft.Icons.ARROW_UPWARD if change >= 0 else ft.Icons.ARROW_DOWNWARD
        change_text = f"+{change}%" if change >= 0 else f"{change}%"
        
        return ft.Container(
            content=ft.Column([
                # Header con icono y título
                ft.Row([
                    ft.Container(
                        content=icon,
                        padding=5,
                        bgcolor=f"{color}20",  # Color con transparencia
                        border_radius=10
                    ),
                    ft.Text(title, expand=True, size=14, color=ft.Colors.GREY),
                ]),
                
                # Valor principal
                ft.Container(
                    content=ft.Text(
                        value,
                        size=28,
                        weight=ft.FontWeight.BOLD,
                        color=COLORS["dark"]
                    ),
                    padding=ft.padding.only(top=10, bottom=5)
                ),
                
                # Cambio porcentual
                ft.Row([
                    ft.Icon(change_icon, size=16, color=change_color),
                    ft.Text(change_text, size=12, color=change_color, weight=ft.FontWeight.W_500),
                    ft.Text(" vs mes anterior", size=12, color=ft.Colors.GREY)
                ], spacing=5)
            ]),
            padding=20,
            bgcolor=ft.Colors.WHITE,
            border_radius=15,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=10,
                color=ft.Colors.BLACK12,
                offset=ft.Offset(0, 2)
            ),
            expand=True
        )


class SalesChartCard:
    @staticmethod
    def create(title: str, data: list, labels: list) -> ft.Container:
        """Crea una tarjeta con gráfico de ventas"""
        # Crear barras del gráfico
        bars = []
        max_value = max(data) if data else 1
        print(data)



        # Manejar caso cuando no hay datos o max_value es 0
        if not data or max(data) == 0:
            max_value = 1  # Valor por defecto para evitar división por cero
        else:
            max_value = max(data)
        
        for value, label in zip(data, labels):
            height = (value / max_value) * 100 if max_value > 0 else 0
            bars.append(
                ft.Column([
                    ft.Text(f"${value:,.0f}" if value > 0 else "$0", size=10),
                    ft.Container(
                        width=25,
                        height=height,
                        bgcolor=COLORS["primary"],
                        border_radius=5
                    ),
                    ft.Text(label, size=11, weight=ft.FontWeight.W_500)
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=5)
            )



        for value, label in zip(data, labels):
            height = (value / max_value) * 100
            bars.append(
                ft.Column([
                    ft.Text(f"${value:,.0f}", size=10),
                    ft.Container(
                        width=25,
                        height=height,
                        bgcolor=COLORS["primary"],
                        border_radius=5
                    ),
                    ft.Text(label, size=11, weight=ft.FontWeight.W_500)
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=5)
            )
        
        return ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Text(title, size=18, weight=ft.FontWeight.BOLD),
                    ft.Container(expand=True),
                    ft.Dropdown(
                        width=120,
                        height=35,
                        options=[
                            ft.dropdown.Option("Últimos 7 días"),
                            ft.dropdown.Option("Últimos 30 días"),
                            ft.dropdown.Option("Últimos 3 meses"),
                        ],
                        value="Últimos 30 días",
                        border_color=COLORS["primary"]
                    )
                ]),
                ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                ft.Container(
                    content=ft.Row(
                        bars,
                        alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                        vertical_alignment=ft.CrossAxisAlignment.END
                    ),
                    height=200,
                    padding=ft.padding.only(bottom=20)
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
            ),
            expand=True
        )


class CategoryCard:
    @staticmethod
    def create(title: str, categories: list, values: list, colors: list) -> ft.Container:
        """Crea una tarjeta de distribución por categorías"""
        items = []
        total = sum(values) if values else 1
        
        for category, value, color in zip(categories, values, colors):
            percentage = (value / total) * 100
            items.append(
                ft.Column([
                    ft.Row([
                        ft.Container(
                            width=12,
                            height=12,
                            bgcolor=color,
                            border_radius=6
                        ),
                        ft.Text(category, size=14, expand=True),
                        ft.Text(f"${value:,.0f}", size=14, weight=ft.FontWeight.BOLD)
                    ]),
                    ft.Container(
                        height=8,
                        expand=True,
                        bgcolor=ft.Colors.GREY_200,
                        border_radius=10,
                        content=ft.Container(
                            width=f"{percentage}%",
                            bgcolor=color,
                            border_radius=10
                        )
                    ),
                    ft.Divider(height=10, color=ft.Colors.TRANSPARENT)
                ], spacing=5)
            )
        
        return ft.Container(
            content=ft.Column([
                ft.Text(title, size=18, weight=ft.FontWeight.BOLD),
                ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                *items,
                ft.Divider(height=10),
                ft.Row([
                    ft.Text("Total:", size=14),
                    ft.Text(f"${total:,.0f}", size=16, weight=ft.FontWeight.BOLD)
                ], alignment=ft.MainAxisAlignment.END)
            ]),
            padding=20,
            bgcolor=ft.Colors.WHITE,
            border_radius=15,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=10,
                color=ft.Colors.BLACK12,
                offset=ft.Offset(0, 2)
            ),
            expand=True
        )


class RecentTransactionsCard:
    @staticmethod
    def create(transactions: list) -> ft.Container:
        """Crea una tarjeta con transacciones recientes"""
        rows = []
        
        for i, trans in enumerate(transactions[:5]):
            rows.append(
                ft.Container(
                    content=ft.Row([
                        ft.Column([
                            ft.Text(trans.get('product_detail', 'N/A'), weight=ft.FontWeight.W_500),
                            ft.Text(trans.get('store_location', 'N/A'), size=12, color=ft.Colors.GREY)
                        ], expand=True),
                        ft.Column([
                            ft.Text(f"${trans.get('Total_Bill', 0):.2f}", weight=ft.FontWeight.BOLD),
                            ft.Text(trans.get('transaction_date', 'N/A'), size=12, color=ft.Colors.GREY)
                        ], horizontal_alignment=ft.CrossAxisAlignment.END)
                    ]),
                    padding=10,
                    bgcolor=ft.Colors.WHITE if i % 2 == 0 else ft.Colors.GREY_50,
                    border_radius=5
                )
            )
        
        return ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Text("Transacciones Recientes", size=18, weight=ft.FontWeight.BOLD),
                    ft.Container(expand=True),
                    ft.ElevatedButton(
                        "Ver Todas",
                        icon=ft.Icons.LIST,
                        style=ft.ButtonStyle(
                            bgcolor=COLORS["primary"],
                            color=ft.Colors.WHITE,
                            padding=ft.padding.symmetric(horizontal=15, vertical=5)
                        )
                    )
                ]),
                ft.Divider(height=20),
                *rows
            ]),
            padding=20,
            bgcolor=ft.Colors.WHITE,
            border_radius=15,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=10,
                color=ft.Colors.BLACK12,
                offset=ft.Offset(0, 2)
            ),
            expand=True
        )