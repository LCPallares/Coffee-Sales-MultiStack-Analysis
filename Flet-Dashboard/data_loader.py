# data_loader.py
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional

class CoffeeDataLoader:
    def __init__(self, filepath: str = "coffee_shop_sales.csv"):
        self.filepath = filepath
        self.df = None
        self.load_data()
        
    def load_data(self):
        """Carga y preprocesa los datos del CSV"""
        try:
            self.df = pd.read_csv(self.filepath)
            self._preprocess_data()
            print(f"Datos cargados: {len(self.df)} registros")
        except Exception as e:
            print(f"Error cargando datos: {e}")
            self.df = pd.DataFrame()
    
    def _preprocess_data(self):
        """Preprocesa los datos para análisis"""
        if self.df is None or self.df.empty:
            return
            
        # Convertir fechas y horas
        self.df['transaction_date'] = pd.to_datetime(self.df['transaction_date'], dayfirst=True)
        self.df['transaction_time'] = pd.to_datetime(self.df['transaction_time'], format='%H:%M:%S').dt.time
        self.df['transaction_datetime'] = pd.to_datetime(
            self.df['transaction_date'].astype(str) + ' ' + self.df['transaction_time'].astype(str)
        )
        
        # Extraer información adicional
        self.df['hour'] = self.df['transaction_datetime'].dt.hour
        self.df['day_of_week'] = self.df['transaction_datetime'].dt.dayofweek
        self.df['month'] = self.df['transaction_datetime'].dt.month
        self.df['day_name'] = self.df['transaction_datetime'].dt.day_name()
        self.df['month_name'] = self.df['transaction_datetime'].dt.month_name()
        
        # Calcular ingresos totales por transacción
        self.df['revenue'] = self.df['transaction_qty'] * self.df['unit_price']
    
    def _is_valid_dataframe(self):
        """Verifica si el DataFrame es válido para operaciones"""
        return self.df is not None and not self.df.empty
    
    def get_summary_stats(self) -> Dict:
        """Obtiene estadísticas resumen"""
        if not self._is_valid_dataframe():
            return {}
            
        return {
            'total_transactions': len(self.df),
            'total_revenue': float(self.df['revenue'].sum()),
            'avg_transaction_value': float(self.df['Total_Bill'].mean()),
            'unique_customers': int(self.df['transaction_id'].nunique()),
            'unique_products': int(self.df['product_id'].nunique()),
            'date_range': {
                'start': self.df['transaction_date'].min(),
                'end': self.df['transaction_date'].max()
            }
        }
    
    def get_daily_sales(self) -> pd.DataFrame:
        """Obtiene ventas diarias"""
        if not self._is_valid_dataframe():
            return pd.DataFrame()
        return self.df.groupby('transaction_date')['revenue'].sum().reset_index()
    
    def get_top_products(self, n: int = 10) -> pd.DataFrame:
        """Obtiene los productos más vendidos"""
        if not self._is_valid_dataframe():
            return pd.DataFrame()
        return self.df.groupby(['product_category', 'product_type', 'product_detail']).agg({
            'transaction_qty': 'sum',
            'revenue': 'sum'
        }).reset_index().sort_values('revenue', ascending=False).head(n)
    
    def get_store_performance(self) -> pd.DataFrame:
        """Obtiene rendimiento por tienda"""
        if not self._is_valid_dataframe():
            return pd.DataFrame()
        return self.df.groupby(['store_id', 'store_location']).agg({
            'transaction_id': 'count',
            'revenue': 'sum',
            'transaction_qty': 'sum'
        }).reset_index()
    
    def get_hourly_sales(self) -> pd.DataFrame:
        """Obtiene ventas por hora del día"""
        if not self._is_valid_dataframe():
            return pd.DataFrame()
        return self.df.groupby('hour')['revenue'].sum().reset_index()
    
    def get_category_sales(self) -> pd.DataFrame:
        """Obtiene ventas por categoría"""
        if not self._is_valid_dataframe():
            return pd.DataFrame()
        return self.df.groupby('product_category')['revenue'].sum().reset_index()
    
    def get_recent_transactions(self, n: int = 10) -> pd.DataFrame:
        """Obtiene transacciones recientes"""
        if not self._is_valid_dataframe():
            return pd.DataFrame()
        return self.df.sort_values('transaction_datetime', ascending=False).head(n)

    def filter_data(self, 
                   start_date=None, 
                   end_date=None,
                   store_ids=None,
                   categories=None,
                   min_price=0,
                   max_price=None) -> pd.DataFrame:
        """Filtra los datos según criterios"""
        if not self._is_valid_dataframe():
            return pd.DataFrame()
            
        df_filtered = self.df.copy()
        
        # Filtrar por fecha
        if start_date:
            df_filtered = df_filtered[df_filtered['transaction_date'] >= start_date]
        if end_date:
            df_filtered = df_filtered[df_filtered['transaction_date'] <= end_date]
        
        # Filtrar por tienda
        if store_ids:
            df_filtered = df_filtered[df_filtered['store_id'].isin(store_ids)]
        
        # Filtrar por categoría
        if categories:
            df_filtered = df_filtered[df_filtered['product_category'].isin(categories)]
        
        # Filtrar por precio
        df_filtered = df_filtered[df_filtered['unit_price'] >= min_price]
        if max_price:
            df_filtered = df_filtered[df_filtered['unit_price'] <= max_price]
        
        return df_filtered
    
    def get_time_period_data(self, period='last_30_days'):
        """Obtiene datos para diferentes períodos de tiempo"""
        from datetime import datetime, timedelta
        
        if not self._is_valid_dataframe():
            return pd.DataFrame()
        
        end_date = self.df['transaction_date'].max()
        
        if period == 'today':
            start_date = end_date
        elif period == 'last_7_days':
            start_date = end_date - timedelta(days=7)
        elif period == 'last_30_days':
            start_date = end_date - timedelta(days=30)
        elif period == 'last_90_days':
            start_date = end_date - timedelta(days=90)
        elif period == 'this_month':
            start_date = end_date.replace(day=1)
        elif period == 'last_month':
            if end_date.day > 1:
                start_date = (end_date.replace(day=1) - timedelta(days=1)).replace(day=1)
                end_date = end_date.replace(day=1) - timedelta(days=1)
            else:
                start_date = end_date.replace(day=1)
                end_date = end_date.replace(day=1)
        elif period == 'all_time':
            start_date = self.df['transaction_date'].min()
        else:
            start_date = self.df['transaction_date'].min()
        
        return self.filter_data(start_date=start_date, end_date=end_date)
    
    def get_unique_values(self, column):
        """Obtiene valores únicos de una columna"""
        if not self._is_valid_dataframe() or column not in self.df.columns:
            return []
        return sorted(self.df[column].dropna().unique().tolist())

