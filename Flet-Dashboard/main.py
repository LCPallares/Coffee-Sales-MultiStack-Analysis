# main.py
import flet as ft
from config import COLORS, PAGES
from data_loader import CoffeeDataLoader
from components.sidebar import Sidebar
from components.header import Header
from pages.dashboard import DashboardPage
from pages.sales import SalesPage
from pages.products import ProductsPage
from pages.analytics import AnalyticsPage  # Crear similar a las otras páginas

class CoffeeShopDashboard:
    def __init__(self, page: ft.Page):
        self.page = page
        self.data_loader = CoffeeDataLoader("../Data/coffee_shop_sales.csv")
        self.setup_page()
        
        # Referencias
        self.content_area = ft.Ref[ft.Container]()
        self.header = Header("Dashboard")
        
        # Inicializar páginas con callbacks
        self.pages = {
            "dashboard": DashboardPage(self.data_loader, self.on_dashboard_filter_change),
            "sales": SalesPage(self.data_loader),
            "products": ProductsPage(self.data_loader),
            "analytics": AnalyticsPage(self.data_loader),
        }
        
        # Barra lateral
        self.sidebar = Sidebar(self.change_page)
        
        # Construir interfaz
        self.build_ui()

    def setup_page(self):
        """Configura la página principal"""
        self.page.title = "Coffee Shop Analytics"
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.padding = 0
        self.page.theme = ft.Theme(
            font_family="Roboto",
            color_scheme_seed=COLORS["primary"]
        )
    
    def build_ui(self):
        """Construye la interfaz de usuario"""
        layout = ft.Row([
            # Barra lateral
            self.sidebar.build(),
            
            # Contenido principal
            ft.Column([
                # Header
                self.header.build(),
                
                # Área de contenido
                ft.Container(
                    ref=self.content_area,
                    content=self.pages["dashboard"].build(),
                    expand=True,
                )
            ], expand=True, spacing=0)
        ], expand=True, spacing=0)
        
        self.page.add(layout)
    
    def on_dashboard_filter_change(self, filters):
        """Callback para cambios en filtros del dashboard"""
        print(f"Filtros actualizados: {filters}")
        # Aquí podrías actualizar otras páginas si es necesario
    
    def change_page(self, page_id: str):
        """Cambia la página actual"""
        if page_id in self.pages:
            self.header.update_title(PAGES[page_id])
            
            # Obtener la página y asignarle referencia a la página principal
            page_instance = self.pages[page_id]
            if hasattr(page_instance, 'page'):
                page_instance.page = self.page
            
            self.content_area.current.content = page_instance.build()
            self.page.update()

def main(page: ft.Page):
    app = CoffeeShopDashboard(page)

if __name__ == "__main__":
    ft.app(
        target=main,
        #view=ft.AppView.WEB_BROWSER,
        assets_dir="assets"
    )