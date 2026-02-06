# pages/dashboard.py
import flet as ft
from config import COLORS
from components.cards import MetricCard, SalesChartCard, CategoryCard, RecentTransactionsCard
from components.filters import FilterPanel

class DashboardPage:
    def __init__(self, data_loader, on_filter_change=None):
        self.data_loader = data_loader
        self.on_filter_change = on_filter_change or (lambda x: None)
        self.current_filters = {}
        
        # Inicializar componentes
        self.filter_panel = FilterPanel(data_loader, self._handle_filter_change)
        self.content_container = ft.Ref[ft.Container]()
    
    def _handle_filter_change(self, filters):
        """Maneja cambios en los filtros"""
        self.current_filters = filters
        self._update_content()
    
    def _update_content(self):
        """Actualiza el contenido con los filtros actuales"""
        if self.content_container.current:
            self.content_container.current.content = self._build_content()
            if hasattr(self, 'page'):
                self.page.update()
    
    def _apply_filters(self):
        """Aplica los filtros actuales a los datos"""
        # Convertir filtros a formato para data_loader
        period_map = {
            'Hoy': 'today',
            'Últimos 7 días': 'last_7_days',
            'Últimos 30 días': 'last_30_days',
            'Últimos 90 días': 'last_90_days',
            'Este mes': 'this_month',
            'Mes anterior': 'last_month',
            'Todo': 'all_time'
        }
        
        period = period_map.get(self.current_filters.get('period', 'Últimos 30 días'), 'last_30_days')
        
        # Obtener datos filtrados
        filtered_df = self.data_loader.get_time_period_data(period)
        
        # Aplicar filtro de tienda
        store = self.current_filters.get('store', 'Todos')
        if store != 'Todos':
            filtered_df = filtered_df[filtered_df['store_location'] == store]
        
        # Aplicar filtro de categoría
        category = self.current_filters.get('category', 'Todos')
        if category != 'Todos':
            filtered_df = filtered_df[filtered_df['product_category'] == category]
        
        return filtered_df
    
    def _build_content(self):
        """Construye el contenido principal"""
        # Obtener datos filtrados
        filtered_df = self._apply_filters()
        
        # Calcular métricas desde datos filtrados
        total_revenue = filtered_df['revenue'].sum()
        total_transactions = len(filtered_df)
        avg_transaction = filtered_df['Total_Bill'].mean() if not filtered_df.empty else 0
        unique_products = filtered_df['product_id'].nunique()
        
        # Obtener datos para gráficos
        daily_sales = filtered_df.groupby('transaction_date')['revenue'].sum().reset_index()
        category_sales = filtered_df.groupby('product_category')['revenue'].sum().reset_index()
        recent_transactions = filtered_df.sort_values('transaction_datetime', ascending=False).head(5)
        
        # Preparar datos para gráficos
        last_7_days = daily_sales.tail(7)
        last_7_days_data = last_7_days['revenue'].tolist() if not last_7_days.empty else []
        last_7_days_labels = last_7_days['transaction_date'].dt.strftime('%d/%m').tolist() if not last_7_days.empty else []
        
        # Tarjetas de métricas con cambios dinámicos
        metric_cards = ft.Row([
            MetricCard.create(
                title="Ingresos Totales",
                value=f"${total_revenue:,.0f}",
                change=self._calculate_change('revenue'),
                icon=ft.Icon(ft.Icons.ATTACH_MONEY, color=COLORS["primary"]),
                color=COLORS["primary"]
            ),
            MetricCard.create(
                title="Transacciones",
                value=f"{total_transactions:,}",
                change=self._calculate_change('transactions'),
                icon=ft.Icon(ft.Icons.RECEIPT, color=COLORS["success"]),
                color=COLORS["success"]
            ),
            MetricCard.create(
                title="Valor Promedio",
                value=f"${avg_transaction:.2f}",
                change=self._calculate_change('avg_value'),
                icon=ft.Icon(ft.Icons.TRENDING_UP, color=COLORS["warning"]),
                color=COLORS["warning"]
            ),
            MetricCard.create(
                title="Productos Únicos",
                value=f"{unique_products:,}",
                change=self._calculate_change('unique_products'),
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
                transactions=recent_transactions.to_dict('records') if not recent_transactions.empty else [],
                on_view_all=self._view_all_transactions
            )
        ])
        
        return content
    
    def _calculate_change(self, metric_type):
        """Calcula el cambio porcentual vs período anterior"""
        # Implementar lógica de comparación con período anterior
        # Por ahora, valores de ejemplo
        changes = {
            'revenue': 12.5,
            'transactions': 8.2,
            'avg_value': -3.1,
            'unique_products': 15.4
        }
        return changes.get(metric_type, 0)
    
    def _view_all_transactions(self, e):
        """Maneja clic en 'Ver Todas' las transacciones"""
        print("Navegar a página de transacciones completas")
        # Aquí podrías cambiar a otra página o mostrar diálogo
    
    def build(self) -> ft.Container:
        """Construye la página completa del dashboard"""
        return ft.Container(
            content=ft.Column([
                # Panel de filtros
                self.filter_panel.build(),
                
                # Contenido principal
                ft.Container(
                    ref=self.content_container,
                    content=self._build_content(),
                    expand=True
                )
            ]),
            padding=20,
            expand=True,
            bgcolor=COLORS["bg"]
        )