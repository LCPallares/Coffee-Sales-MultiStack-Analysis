# pages/products.py
import flet as ft
from config import COLORS
from components.cards import CategoryCard

class ProductsPage:
    def __init__(self, data_loader):
        self.data_loader = data_loader
    
    def build(self) -> ft.Container:
        """Construye la página de productos"""
        # Obtener datos
        top_products = self.data_loader.get_top_products(10)
        category_sales = self.data_loader.get_category_sales()
        
        # Tabla de productos más vendidos
        product_rows = []
        if not top_products.empty:
            for i, (_, product) in enumerate(top_products.iterrows()):
                product_rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(str(i + 1))),
                            ft.DataCell(ft.Text(product['product_category'])),
                            ft.DataCell(ft.Text(product['product_type'])),
                            ft.DataCell(ft.Text(product['product_detail'])),
                            ft.DataCell(ft.Text(f"{int(product['transaction_qty']):,}")),
                            ft.DataCell(ft.Text(f"${product['revenue']:,.0f}")),
                            ft.DataCell(
                                ft.Row([
                                    ft.IconButton(
                                        icon=ft.Icons.EDIT,
                                        icon_color=COLORS["primary"],
                                        icon_size=20,
                                        tooltip="Editar"
                                    ),
                                    ft.IconButton(
                                        icon=ft.Icons.DELETE,
                                        icon_color=ft.Colors.RED,
                                        icon_size=20,
                                        tooltip="Eliminar"
                                    ),
                                ], spacing=5)
                            ),
                        ]
                    )
                )
        
        products_table = ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Text("Productos Más Vendidos", size=20, weight=ft.FontWeight.BOLD),
                    ft.Container(expand=True),
                    ft.ElevatedButton(
                        "Exportar Reporte",
                        icon=ft.Icons.DOWNLOAD,
                        style=ft.ButtonStyle(
                            bgcolor=COLORS["primary"],
                            color=ft.Colors.WHITE
                        )
                    )
                ]),
                ft.Divider(height=20),
                ft.DataTable(
                    columns=[
                        ft.DataColumn(ft.Text("#")),
                        ft.DataColumn(ft.Text("Categoría")),
                        ft.DataColumn(ft.Text("Tipo")),
                        ft.DataColumn(ft.Text("Detalle")),
                        ft.DataColumn(ft.Text("Cantidad")),
                        ft.DataColumn(ft.Text("Ingresos")),
                        ft.DataColumn(ft.Text("Acciones")),
                    ],
                    rows=product_rows,
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
        
        # Gráfico de categorías
        category_card = CategoryCard.create(
            title="Distribución por Categoría",
            categories=category_sales['product_category'].tolist() if not category_sales.empty else [],
            values=category_sales['revenue'].tolist() if not category_sales.empty else [],
            colors=[COLORS["primary"], COLORS["secondary"], COLORS["success"], 
                   COLORS["warning"], COLORS["info"], COLORS["danger"]]
        )
        
        # Análisis por tamaño
        size_analysis = ft.Container(
            content=ft.Column([
                ft.Text("Análisis por Tamaño", size=20, weight=ft.FontWeight.BOLD),
                ft.Divider(height=20),
                ft.Row([
                    ft.Column([
                        ft.Text("Small", size=16),
                        ft.Text("15%", size=24, weight=ft.FontWeight.BOLD)
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    ft.Column([
                        ft.Text("Medium", size=16),
                        ft.Text("45%", size=24, weight=ft.FontWeight.BOLD)
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    ft.Column([
                        ft.Text("Large", size=16),
                        ft.Text("40%", size=24, weight=ft.FontWeight.BOLD)
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                ], spacing=50, alignment=ft.MainAxisAlignment.CENTER)
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
        
        # Contenido completo
        content = ft.Column([
            ft.Row([
                category_card,
                size_analysis
            ], spacing=20),
            ft.Divider(height=30, color=ft.Colors.TRANSPARENT),
            products_table
        ])
        
        return ft.Container(
            content=content,
            padding=20,
            expand=True,
            bgcolor=COLORS["bg"]
        )