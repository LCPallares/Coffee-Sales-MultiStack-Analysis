"""
Data loading and preparation utilities
"""

import pandas as pd
import numpy as np
from datetime import datetime

def load_and_prepare_data(filepath):
    """
    Load and prepare the coffee shop sales data
    
    Parameters:
    -----------
    filepath : str
        Path to the CSV file
        
    Returns:
    --------
    pd.DataFrame
        Prepared dataframe with proper dtypes and calculated fields
    """
    
    # Read the CSV
    df = pd.read_csv(filepath)
    
    # Convert date columns
    # Handle both date formats in the data
    df['transaction_date'] = pd.to_datetime(
        df['transaction_date'], 
        format='mixed',
        dayfirst=True
    )
    
    # Convert time to datetime for easier manipulation
    df['transaction_time'] = pd.to_datetime(
        df['transaction_time'], 
        format='%H:%M:%S'
    ).dt.time
    
    # Create datetime column combining date and time
    df['transaction_datetime'] = pd.to_datetime(
        df['transaction_date'].astype(str) + ' ' + df['transaction_time'].astype(str)
    )
    
    # Ensure numeric columns are proper type
    numeric_cols = ['transaction_qty', 'unit_price', 'Total_Bill', 'Hour', 'Month', 'Day of Week']
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # Add calculated fields
    df['revenue'] = df['transaction_qty'] * df['unit_price']
    
    # Add time-based features
    df['week'] = df['transaction_date'].dt.isocalendar().week
    df['quarter'] = df['transaction_date'].dt.quarter
    df['is_weekend'] = df['Day of Week'].isin([5, 6])  # Saturday=5, Sunday=6
    
    # Add time period classification
    df['time_period'] = df['Hour'].apply(classify_time_period)
    
    # Sort by date
    df = df.sort_values('transaction_datetime')
    
    return df

def classify_time_period(hour):
    """Classify hour into time periods"""
    if 6 <= hour < 11:
        return 'Morning'
    elif 11 <= hour < 14:
        return 'Lunch'
    elif 14 <= hour < 17:
        return 'Afternoon'
    elif 17 <= hour < 20:
        return 'Evening'
    else:
        return 'Night'

def get_date_range(df):
    """Get the min and max dates from the dataframe"""
    return df['transaction_date'].min(), df['transaction_date'].max()

def calculate_metrics(df):
    """
    Calculate key business metrics from the dataframe
    
    Parameters:
    -----------
    df : pd.DataFrame
        Filtered dataframe
        
    Returns:
    --------
    dict
        Dictionary containing calculated metrics
    """
    
    metrics = {
        'total_revenue': df['Total_Bill'].sum(),
        'total_transactions': len(df),
        'total_quantity': df['transaction_qty'].sum(),
        'avg_transaction': df['Total_Bill'].mean(),
        'avg_items_per_transaction': df['transaction_qty'].mean(),
        'unique_products': df['product_detail'].nunique(),
        'unique_customers': len(df),  # Each transaction as a customer visit
    }
    
    # Calculate growth rates if enough data
    if len(df) > 30:
        df_sorted = df.sort_values('transaction_date')
        recent = df_sorted.tail(len(df_sorted)//2)
        previous = df_sorted.head(len(df_sorted)//2)
        
        metrics['revenue_growth'] = (
            (recent['Total_Bill'].sum() - previous['Total_Bill'].sum()) / 
            previous['Total_Bill'].sum() * 100
        )
        metrics['transaction_growth'] = (
            (len(recent) - len(previous)) / len(previous) * 100
        )
    else:
        metrics['revenue_growth'] = 0
        metrics['transaction_growth'] = 0
    
    return metrics

def get_top_products(df, n=10):
    """Get top N products by revenue"""
    return (
        df.groupby('product_detail')
        .agg({
            'Total_Bill': 'sum',
            'transaction_qty': 'sum',
            'transaction_id': 'count'
        })
        .sort_values('Total_Bill', ascending=False)
        .head(n)
        .reset_index()
    )

def get_category_summary(df):
    """Get summary statistics by category"""
    return (
        df.groupby('product_category')
        .agg({
            'Total_Bill': 'sum',
            'transaction_qty': 'sum',
            'transaction_id': 'count',
            'unit_price': 'mean'
        })
        .reset_index()
    )
