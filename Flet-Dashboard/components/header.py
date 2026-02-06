# components/header.py
import flet as ft
from datetime import datetime
from config import COLORS

class Header:
    def __init__(self, page_title: str = "Dashboard"):
        self.page_title = page_title
        self.last_update = datetime.now()
        
    def build(self) -> ft.Container:
        """Construye el header"""
        return ft.Container(
            content=ft.Row([
                # Título de la página
                ft.Column([
                    ft.Text(
                        self.page_title,
                        size=24,
                        weight=ft.FontWeight.BOLD,
                        color=COLORS["dark"]
                    ),
                    ft.Text(
                        f"Última actualización: {self.last_update.strftime('%d/%m/%Y %H:%M')}",
                        size=12,
                        color=ft.Colors.GREY
                    )
                ], expand=True),
                
                # Controles del header
                ft.Row([
                    # Búsqueda
                    ft.Container(
                        content=ft.TextField(
                            hint_text="Buscar...",
                            prefix_icon=ft.Icons.SEARCH,
                            width=200,
                            height=40,
                            border_radius=20,
                            border_color=ft.Colors.GREY_300,
                            filled=True,
                            fill_color=ft.Colors.WHITE
                        ),
                        padding=ft.padding.only(right=10)
                    ),
                    
                    # Notificaciones
                    ft.IconButton(
                        icon=ft.Icons.NOTIFICATIONS,
                        icon_color=COLORS["primary"],
                        tooltip="Notificaciones"
                    ),
                    
                    # Configuración
                    ft.IconButton(
                        icon=ft.Icons.SETTINGS,
                        icon_color=COLORS["primary"],
                        tooltip="Configuración"
                    ),
                    
                    # Perfil con menú
                    ft.PopupMenuButton(
                        icon=ft.Icons.MORE_VERT,
                        items=[
                            ft.PopupMenuItem(text="Perfil"),
                            ft.PopupMenuItem(text="Configuración"),
                            ft.PopupMenuItem(),
                            ft.PopupMenuItem(text="Cerrar sesión"),
                        ]
                    )
                ], spacing=5)
            ]),
            padding=20,
            bgcolor=ft.Colors.WHITE,
            border=ft.border.only(bottom=ft.border.BorderSide(1, ft.Colors.GREY_300))
        )
    
    def update_title(self, new_title: str):
        """Actualiza el título del header"""
        self.page_title = new_title
        self.last_update = datetime.now()