# data_loader.py
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
import os

class CoffeeDataLoader:
    def __init__(self, filepath: str = "coffee_shop_sales.csv"):
        self.filepath = filepath
        self.df = None
        self.load_data()
        
    def load_data(self):
        """Carga y preprocesa los datos del CSV"""
        try:
            #self.base_path = os.path.dirname(__file__)
            #self.file_path = os.path.join(self.base_path, "..", "Data", "coffee_shop_sales.csv")
            self.df = pd.read_csv(self.filepath)
            self._preprocess_data()
            print(f"Datos cargados: {len(self.df)} registros")
        except Exception as e:
            print(f"Error cargando datos: {e}")
            self.df = pd.DataFrame()
    
    def _preprocess_data(self):
        """Preprocesa los datos para análisis"""
        if self.df.empty:
            return
            
        # Convertir fechas y horas
        #self.df['transaction_date'] = pd.to_datetime(self.df['transaction_date'])
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
    
    def get_summary_stats(self) -> Dict:
        """Obtiene estadísticas resumen"""
        if self.df.empty:
            return {}
            
        return {
            'total_transactions': len(self.df),
            'total_revenue': self.df['revenue'].sum(),
            'avg_transaction_value': self.df['Total_Bill'].mean(),
            'unique_customers': self.df['transaction_id'].nunique(),
            'unique_products': self.df['product_id'].nunique(),
            'date_range': {
                'start': self.df['transaction_date'].min(),
                'end': self.df['transaction_date'].max()
            }
        }
    
    def get_daily_sales(self) -> pd.DataFrame:
        """Obtiene ventas diarias"""
        if self.df.empty:
            return pd.DataFrame()
        return self.df.groupby('transaction_date')['revenue'].sum().reset_index()
    
    def get_top_products(self, n: int = 10) -> pd.DataFrame:
        """Obtiene los productos más vendidos"""
        if self.df.empty:
            return pd.DataFrame()
        return self.df.groupby(['product_category', 'product_type', 'product_detail']).agg({
            'transaction_qty': 'sum',
            'revenue': 'sum'
        }).reset_index().sort_values('revenue', ascending=False).head(n)
    
    def get_store_performance(self) -> pd.DataFrame:
        """Obtiene rendimiento por tienda"""
        if self.df.empty:
            return pd.DataFrame()
        return self.df.groupby(['store_id', 'store_location']).agg({
            'transaction_id': 'count',
            'revenue': 'sum',
            'transaction_qty': 'sum'
        }).reset_index()
    
    def get_hourly_sales(self) -> pd.DataFrame:
        """Obtiene ventas por hora del día"""
        if self.df.empty:
            return pd.DataFrame()
        return self.df.groupby('hour')['revenue'].sum().reset_index()
    
    def get_category_sales(self) -> pd.DataFrame:
        """Obtiene ventas por categoría"""
        if self.df.empty:
            return pd.DataFrame()
        return self.df.groupby('product_category')['revenue'].sum().reset_index()
    
    def get_recent_transactions(self, n: int = 10) -> pd.DataFrame:
        """Obtiene transacciones recientes"""
        if self.df.empty:
            return pd.DataFrame()
        return self.df.sort_values('transaction_datetime', ascending=False).head(n)