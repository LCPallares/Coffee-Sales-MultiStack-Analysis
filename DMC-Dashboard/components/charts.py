"""
Chart components for the dashboard
Each function creates a specific visualization
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import dcc, html
import dash_mantine_components as dmc
from utils.theme import style_chart, CHART_COLORS

def create_sales_trend(df):
    """
    Create a time series chart showing sales trend over time
    """
    
    # Aggregate by date
    daily_sales = df.groupby('transaction_date').agg({
        'Total_Bill': 'sum',
        'transaction_id': 'count'
    }).reset_index()
    
    # Create figure with secondary y-axis
    fig = go.Figure()
    
    # Revenue line
    fig.add_trace(
        go.Scatter(
            x=daily_sales['transaction_date'],
            y=daily_sales['Total_Bill'],
            name='Revenue',
            mode='lines+markers',
            line=dict(color=CHART_COLORS['primary'], width=3),
            marker=dict(size=6),
            yaxis='y',
            hovertemplate='<b>%{x|%B %d}</b><br>Revenue: $%{y:,.2f}<extra></extra>'
        )
    )
    
    # Transactions line
    fig.add_trace(
        go.Scatter(
            x=daily_sales['transaction_date'],
            y=daily_sales['transaction_id'],
            name='Transactions',
            mode='lines+markers',
            line=dict(color=CHART_COLORS['secondary'], width=2, dash='dash'),
            marker=dict(size=4),
            yaxis='y2',
            hovertemplate='<b>%{x|%B %d}</b><br>Transactions: %{y}<extra></extra>'
        )
    )
    
    # Update layout with dual y-axes
    fig.update_layout(
        yaxis=dict(
            title='Revenue ($)',
            titlefont=dict(color=CHART_COLORS['primary']),
            tickfont=dict(color=CHART_COLORS['primary'])
        ),
        yaxis2=dict(
            title='Transactions',
            titlefont=dict(color=CHART_COLORS['secondary']),
            tickfont=dict(color=CHART_COLORS['secondary']),
            overlaying='y',
            side='right'
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    fig = style_chart(fig, title="Sales Trend Over Time", height=400)
    
    return dcc.Graph(figure=fig, config={'displayModeBar': False})

def create_category_distribution(df):
    """
    Create a pie chart showing revenue distribution by category
    """
    
    category_sales = df.groupby('product_category')['Total_Bill'].sum().reset_index()
    category_sales = category_sales.sort_values('Total_Bill', ascending=False)
    
    fig = go.Figure(
        data=[
            go.Pie(
                labels=category_sales['product_category'],
                values=category_sales['Total_Bill'],
                hole=0.4,
                marker=dict(
                    colors=['#8B4513', '#D4B896', '#C09F76', '#A67C52', '#6F3609'],
                    line=dict(color='white', width=2)
                ),
                textposition='auto',
                textinfo='label+percent',
                hovertemplate='<b>%{label}</b><br>Revenue: $%{value:,.2f}<br>Share: %{percent}<extra></extra>'
            )
        ]
    )
    
    fig = style_chart(fig, title="Revenue by Category", height=400)
    
    return dcc.Graph(figure=fig, config={'displayModeBar': False})

def create_hourly_heatmap(df):
    """
    Create a heatmap showing sales patterns by hour and day of week
    """
    
    # Create pivot table
    heatmap_data = df.groupby(['Day Name', 'Hour'])['Total_Bill'].sum().reset_index()
    heatmap_pivot = heatmap_data.pivot(index='Hour', columns='Day Name', values='Total_Bill')
    
    # Order days correctly
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    heatmap_pivot = heatmap_pivot.reindex(columns=[d for d in day_order if d in heatmap_pivot.columns])
    
    fig = go.Figure(
        data=go.Heatmap(
            z=heatmap_pivot.values,
            x=heatmap_pivot.columns,
            y=heatmap_pivot.index,
            colorscale=[
                [0, '#F5E6D3'],
                [0.2, '#E8D4BB'],
                [0.4, '#D4B896'],
                [0.6, '#A67C52'],
                [0.8, '#8B4513'],
                [1, '#6F3609']
            ],
            hovertemplate='<b>%{x}</b><br>Hour: %{y}:00<br>Revenue: $%{z:,.2f}<extra></extra>',
            colorbar=dict(title="Revenue")
        )
    )
    
    fig.update_layout(
        xaxis=dict(side='bottom'),
        yaxis=dict(autorange='reversed')
    )
    
    fig = style_chart(fig, title="Sales Heatmap by Hour & Day", height=450)
    
    return dcc.Graph(figure=fig, config={'displayModeBar': False})

def create_top_products(df, n=10):
    """
    Create a horizontal bar chart showing top products by revenue
    """
    
    top_products = (
        df.groupby('product_detail')['Total_Bill']
        .sum()
        .sort_values(ascending=True)
        .tail(n)
        .reset_index()
    )
    
    fig = go.Figure(
        data=[
            go.Bar(
                y=top_products['product_detail'],
                x=top_products['Total_Bill'],
                orientation='h',
                marker=dict(
                    color=top_products['Total_Bill'],
                    colorscale=[
                        [0, '#E8D4BB'],
                        [0.5, '#A67C52'],
                        [1, '#8B4513']
                    ],
                    line=dict(color='white', width=1)
                ),
                hovertemplate='<b>%{y}</b><br>Revenue: $%{x:,.2f}<extra></extra>'
            )
        ]
    )
    
    fig.update_layout(
        yaxis=dict(tickfont=dict(size=11)),
        xaxis=dict(title='Revenue ($)')
    )
    
    fig = style_chart(fig, title=f"Top {n} Products by Revenue", height=450)
    
    return dcc.Graph(figure=fig, config={'displayModeBar': False})

def create_store_comparison(df):
    """
    Create a bar chart comparing performance across stores
    """
    
    store_metrics = df.groupby('store_location').agg({
        'Total_Bill': 'sum',
        'transaction_id': 'count'
    }).reset_index()
    
    store_metrics['avg_transaction'] = (
        store_metrics['Total_Bill'] / store_metrics['transaction_id']
    )
    
    fig = go.Figure()
    
    # Revenue bars
    fig.add_trace(
        go.Bar(
            name='Total Revenue',
            x=store_metrics['store_location'],
            y=store_metrics['Total_Bill'],
            marker_color=CHART_COLORS['primary'],
            hovertemplate='<b>%{x}</b><br>Revenue: $%{y:,.2f}<extra></extra>'
        )
    )
    
    fig.update_layout(
        yaxis=dict(title='Revenue ($)'),
        xaxis=dict(title='Store Location'),
        showlegend=False
    )
    
    fig = style_chart(fig, title="Store Performance Comparison", height=400)
    
    return dcc.Graph(figure=fig, config={'displayModeBar': False})

def create_weekday_analysis(df):
    """
    Create a bar chart showing sales patterns by day of week
    """
    
    # Order days correctly
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    
    weekday_sales = df.groupby('Day Name').agg({
        'Total_Bill': 'sum',
        'transaction_id': 'count'
    }).reset_index()
    
    # Ensure correct order
    weekday_sales['Day Name'] = pd.Categorical(
        weekday_sales['Day Name'],
        categories=day_order,
        ordered=True
    )
    weekday_sales = weekday_sales.sort_values('Day Name')
    
    fig = go.Figure()
    
    fig.add_trace(
        go.Bar(
            x=weekday_sales['Day Name'],
            y=weekday_sales['Total_Bill'],
            marker=dict(
                color=['#8B4513', '#A67C52', '#C09F76', '#D4B896', '#8B4513', '#6F3609', '#5C2D08'],
                line=dict(color='white', width=1)
            ),
            hovertemplate='<b>%{x}</b><br>Revenue: $%{y:,.2f}<extra></extra>'
        )
    )
    
    fig.update_layout(
        yaxis=dict(title='Revenue ($)'),
        xaxis=dict(title='Day of Week'),
        showlegend=False
    )
    
    fig = style_chart(fig, title="Weekly Sales Pattern", height=400)
    
    return dcc.Graph(figure=fig, config={'displayModeBar': False})
