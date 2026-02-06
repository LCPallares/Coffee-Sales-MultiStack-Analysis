# pages/analytics.py
import flet as ft
from config import COLORS

class AnalyticsPage:
    def __init__(self, data_loader):
        self.data_loader = data_loader
    
    def build(self) -> ft.Container:
        """Construye la página de analytics"""
        return ft.Container(
            content=ft.Column([
                ft.Text("Analytics Avanzados", size=28, weight=ft.FontWeight.BOLD),
                ft.Divider(height=20),
                ft.Text("Página en construcción...", size=18)
            ]),
            padding=20,
            expand=True,
            bgcolor=COLORS["bg"]
        )