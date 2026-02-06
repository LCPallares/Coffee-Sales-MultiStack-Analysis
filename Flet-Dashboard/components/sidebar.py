# components/sidebar.py
import flet as ft
from config import COLORS, PAGES, PAGE_ICONS

class Sidebar:
    def __init__(self, on_page_change):
        self.on_page_change = on_page_change
        self.current_page = "dashboard"
        
    def build(self) -> ft.Container:
        """Construye la barra lateral"""
        menu_items = []
        
        for page_id, page_name in PAGES.items():
            is_selected = page_id == self.current_page
            
            # Crear el ListTile sin border_radius
            list_tile = ft.ListTile(
                leading=ft.Icon(
                    PAGE_ICONS.get(page_id, ft.Icons.DASHBOARD),
                    color=COLORS["primary"] if is_selected else ft.Colors.GREY
                ),
                title=ft.Text(
                    page_name,
                    weight=ft.FontWeight.BOLD if is_selected else ft.FontWeight.NORMAL,
                    color=COLORS["primary"] if is_selected else ft.Colors.BLACK
                ),
                on_click=lambda e, page=page_id: self._change_page(page),
            )
            
            # Envolver en un Container si está seleccionado
            if is_selected:
                menu_items.append(
                    ft.Container(
                        content=list_tile,
                        bgcolor=ft.Colors.BLUE_50,
                        border_radius=10,
                        margin=ft.margin.symmetric(vertical=2, horizontal=10)
                    )
                )
            else:
                menu_items.append(
                    ft.Container(
                        content=list_tile,
                        margin=ft.margin.symmetric(vertical=2, horizontal=10)
                    )
                )
        
        return ft.Container(
            content=ft.Column([
                # Logo y título
                ft.Container(
                    content=ft.Row([
                        ft.Icon(ft.Icons.COFFEE, color=COLORS["primary"], size=30),
                        ft.Column([
                            ft.Text("Coffee Shop", size=18, weight=ft.FontWeight.BOLD),
                            ft.Text("Analytics", size=12, color=COLORS["secondary"])
                        ], spacing=0)
                    ]),
                    padding=ft.padding.only(top=20, left=20, right=20, bottom=30)
                ),
                
                # Menú de navegación
                ft.Column(menu_items, spacing=5),
                
                # Espacio flexible
                ft.Container(expand=True),
                
                # Panel de usuario
                self._build_user_panel(),
                
                # Pie de página
                ft.Container(
                    content=ft.Column([
                        ft.Divider(height=1),
                        ft.Container(
                            content=ft.Text(
                                "© 2024 Coffee Analytics",
                                size=10,
                                color=ft.Colors.GREY
                            ),
                            padding=10,
                            alignment=ft.alignment.center
                        )
                    ])
                )
            ]),
            width=250,
            bgcolor=COLORS["light"],
            border=ft.border.only(right=ft.border.BorderSide(1, ft.Colors.GREY_300))
        )
    
    def _build_user_panel(self) -> ft.Container:
        """Construye el panel de usuario"""
        return ft.Container(
            content=ft.Column([
                ft.Divider(height=20),
                ft.Container(
                    content=ft.Row([
                        ft.CircleAvatar(
                            foreground_image_url="https://randomuser.me/api/portraits/men/32.jpg",
                            radius=20
                        ),
                        ft.Column([
                            ft.Text("Manager", size=14, weight=ft.FontWeight.BOLD),
                            ft.Text("Coffee Shop Admin", size=12, color=ft.Colors.GREY)
                        ], spacing=0)
                    ], spacing=10),
                    padding=ft.padding.symmetric(horizontal=20, vertical=10),
                ),
                ft.Container(
                    content=ft.ElevatedButton(
                        "Actualizar Datos",
                        icon=ft.Icons.REFRESH,
                        style=ft.ButtonStyle(
                            bgcolor=COLORS["primary"],
                            color=ft.Colors.WHITE
                        ),
                        width=200
                    ),
                    padding=ft.padding.only(bottom=20),
                    alignment=ft.alignment.center
                )
            ])
        )
    
    def _change_page(self, page_id: str):
        """Cambia la página actual"""
        self.current_page = page_id
        self.on_page_change(page_id)