"""
Chart components for the dashboard
Each function creates a specific visualization
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
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


def create_size_distribution(df):
    """
    Create a donut chart showing revenue distribution by product size
    """

    size_sales = df.groupby('Size')['Total_Bill'].sum().reset_index()
    size_sales = size_sales.sort_values('Total_Bill', ascending=False)

    fig = go.Figure(
        data=[
            go.Pie(
                labels=size_sales['Size'],
                values=size_sales['Total_Bill'],
                hole=0.5,
                marker=dict(
                    colors=['#8B4513', '#C09F76', '#D4B896'],
                    line=dict(color='white', width=2)
                ),
                textposition='auto',
                textinfo='label+percent',
                hovertemplate='<b>%{label}</b><br>Revenue: $%{value:,.2f}<br>%{percent}<extra></extra>'
            )
        ]
    )

    fig = style_chart(fig, title="Revenue by Size", height=400)

    return dcc.Graph(figure=fig, config={'displayModeBar': False})


def create_monthly_trend(df):
    """
    Create monthly trend chart with average line
    """
    
    month_order = ['January', 'February', 'March', 'April', 'May', 'June',
                   'July', 'August', 'September', 'October', 'November', 'December']
    
    monthly_sales = df.groupby('Month Name')['Total_Bill'].sum().reset_index()
    monthly_sales['Month Name'] = pd.Categorical(
        monthly_sales['Month Name'],
        categories=month_order,
        ordered=True
    )
    monthly_sales = monthly_sales.sort_values('Month Name')
    
    average = monthly_sales['Total_Bill'].mean()
    
    # Color based on average
    colors = ['#59270E' if val >= average else '#c3a689' for val in monthly_sales['Total_Bill']]
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=monthly_sales['Month Name'],
        y=monthly_sales['Total_Bill'],
        marker_color=colors,
        hovertemplate='<b>%{x}</b><br>Revenue: $%{y:,.2f}<extra></extra>'
    ))
    
    # Add average line
    fig.add_hline(
        y=average, 
        line_dash="dot", 
        line_color="#3d2b1f",
        annotation_text=f"Average: ${average:,.0f}",
        annotation_position="right"
    )
    
    fig.update_layout(
        yaxis=dict(title='Revenue ($)'),
        xaxis=dict(title='Month'),
        showlegend=False
    )
    
    fig = style_chart(fig, title="Monthly Trend (Global)", height=400)
    
    return dcc.Graph(figure=fig, config={'displayModeBar': False})

def create_daily_sales_bar(df, month_name=None):
    """
    Create daily sales bar chart with average line
    """
    
    daily = df.groupby('Day')['Total_Bill'].sum().reset_index()
    avg_val = daily['Total_Bill'].mean()
    
    colors = ['#59270E' if val >= avg_val else '#c3a689' for val in daily['Total_Bill']]
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=daily['Day'],
        y=daily['Total_Bill'],
        marker_color=colors,
        hovertemplate='<b>Day %{x}</b><br>Revenue: $%{y:,.2f}<extra></extra>'
    ))
    
    fig.add_hline(
        y=avg_val,
        line_dash="dot",
        line_color="#3d2b1f",
        annotation_text=f"Average: ${avg_val:,.0f}",
        annotation_position="right"
    )
    
    fig.update_layout(
        yaxis=dict(title='Revenue ($)'),
        xaxis=dict(title='Day of Month', range=[0.5, 31.5]),
        showlegend=False
    )
    
    title = f"Daily Sales - {month_name}" if month_name else "Daily Sales"
    fig = style_chart(fig, title=title, height=400)
    
    return dcc.Graph(figure=fig, config={'displayModeBar': False})

def create_category_comparison(df_current, df_previous):
    """
    Create comparative bar chart for current vs previous period by category
    """
    
    if df_previous.empty:
        return html.Div(
            dmc.Alert(
                "No previous period data available for comparison",
                title="Info",
                color="blue"
            )
        )
    
    # Group by category
    cat_current = df_current.groupby('product_category')['Total_Bill'].sum().reset_index()
    cat_previous = df_previous.groupby('product_category')['Total_Bill'].sum().reset_index()
    
    # Merge
    df_comp = pd.merge(
        cat_current, 
        cat_previous, 
        on='product_category', 
        how='outer', 
        suffixes=('_Current', '_Previous')
    ).fillna(0)
    
    df_comp = df_comp.sort_values('Total_Bill_Current', ascending=True)
    
    fig = go.Figure()
    
    # Previous period bars (light)
    fig.add_trace(go.Bar(
        y=df_comp['product_category'],
        x=df_comp['Total_Bill_Previous'],
        name='Previous Period',
        orientation='h',
        marker_color='#c3a689'
    ))
    
    # Current period bars (dark)
    fig.add_trace(go.Bar(
        y=df_comp['product_category'],
        x=df_comp['Total_Bill_Current'],
        name='Current Period',
        orientation='h',
        marker_color='#59270E'
    ))
    
    fig.update_layout(
        barmode='group',
        yaxis=dict(title=''),
        xaxis=dict(title='Revenue ($)'),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    fig = style_chart(fig, title="Category Comparison: Current vs Previous", height=450)
    
    return dcc.Graph(figure=fig, config={'displayModeBar': False})

def create_category_variation(df_current, df_previous):
    """
    Create variation chart showing difference between periods
    """
    
    if df_previous.empty:
        return html.Div(
            dmc.Alert(
                "No previous period data for comparison",
                title="Info",
                color="blue"
            )
        )
    
    cat_current = df_current.groupby('product_category')['Total_Bill'].sum()
    cat_previous = df_previous.groupby('product_category')['Total_Bill'].sum()
    
    df_diff = pd.DataFrame({
        'Current': cat_current,
        'Previous': cat_previous
    }).fillna(0)
    
    df_diff['Difference'] = df_diff['Current'] - df_diff['Previous']
    df_diff = df_diff.sort_values('Difference', ascending=True).reset_index()
    
    colors = ['#59270E' if x > 0 else '#c3a689' for x in df_diff['Difference']]
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=df_diff['Difference'],
        y=df_diff['product_category'],
        orientation='h',
        marker_color=colors,
        text=df_diff['Difference'],
        texttemplate='$%{text:.2s}',
        textposition='outside',
        hovertemplate='<b>%{y}</b><br>Difference: $%{x:,.2f}<extra></extra>'
    ))
    
    fig.update_layout(
        yaxis=dict(title=''),
        xaxis=dict(title='Difference ($)'),
        showlegend=False
    )
    
    fig = style_chart(fig, title="Sales Variation vs Previous Period", height=400)
    
    return dcc.Graph(figure=fig, config={'displayModeBar': False})

def create_heatmap_with_totals(df):
    """
    Create enhanced heatmap with row and column totals
    """
    
    # Create pivot table
    heatmap_data = df.groupby(['Day Name', 'Hour'])['Total_Bill'].sum().reset_index()
    heatmap_pivot = heatmap_data.pivot(index='Hour', columns='Day Name', values='Total_Bill')
    
    # Order days
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    heatmap_pivot = heatmap_pivot.reindex(columns=[d for d in day_order if d in heatmap_pivot.columns])
    
    # Calculate totals
    row_totals = heatmap_pivot.sum(axis=1)
    col_totals = heatmap_pivot.sum(axis=0)
    
    # Add totals to pivot
    heatmap_pivot['Total'] = row_totals
    heatmap_pivot.loc['Total'] = heatmap_pivot.sum()
    
    fig = go.Figure(
        data=go.Heatmap(
            z=heatmap_pivot.values,
            x=list(heatmap_pivot.columns),
            y=list(heatmap_pivot.index),
            colorscale=[
                [0, '#F5E6D3'],
                [0.2, '#E8D4BB'],
                [0.4, '#D4B896'],
                [0.6, '#A67C52'],
                [0.8, '#8B4513'],
                [1, '#6F3609']
            ],
            hovertemplate='<b>%{x}</b><br>Hour: %{y}<br>Revenue: $%{z:,.2f}<extra></extra>',
            colorbar=dict(title="Revenue ($)")
        )
    )
    
    fig.update_layout(
        xaxis=dict(side='bottom'),
        yaxis=dict(autorange='reversed')
    )
    
    fig = style_chart(fig, title="Sales Heatmap by Hour & Day (with Totals)", height=500)
    
    return dcc.Graph(figure=fig, config={'displayModeBar': False})

def create_price_transaction_analysis(df):
    """
    Create scatter plot analyzing price vs transaction quantity
    """
    
    fig = px.scatter(
        df,
        x='unit_price',
        y='transaction_qty',
        size='Total_Bill',
        color='product_category',
        hover_data=['product_detail'],
        color_discrete_sequence=['#8B4513', '#D4B896', '#C09F76', '#A67C52', '#6F3609'],
        labels={
            'unit_price': 'Unit Price ($)',
            'transaction_qty': 'Quantity',
            'product_category': 'Category'
        }
    )
    
    fig.update_layout(
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.3,
            xanchor="center",
            x=0.5
        )
    )
    
    fig = style_chart(fig, title="Price vs Transaction Quantity Analysis", height=450)
    
    return dcc.Graph(figure=fig, config={'displayModeBar': False})

def create_category_price_qty_quadrants(df):
    """
    Create quadrant analysis for category pricing and quantity
    """
    
    category_summary = df.groupby('product_category').agg({
        'unit_price': 'mean',
        'transaction_qty': 'sum',
        'Total_Bill': 'sum'
    }).reset_index()
    
    avg_price = category_summary['unit_price'].mean()
    avg_qty = category_summary['transaction_qty'].mean()
    
    fig = go.Figure()
    
    # Add quadrant lines
    fig.add_hline(y=avg_qty, line_dash="dash", line_color="gray", opacity=0.5)
    fig.add_vline(x=avg_price, line_dash="dash", line_color="gray", opacity=0.5)
    
    # Add scatter points
    fig.add_trace(go.Scatter(
        x=category_summary['unit_price'],
        y=category_summary['transaction_qty'],
        mode='markers+text',
        marker=dict(
            size=category_summary['Total_Bill'] / 100,
            color=category_summary['Total_Bill'],
            colorscale='Burg',
            showscale=True,
            colorbar=dict(title="Revenue")
        ),
        text=category_summary['product_category'],
        textposition='top center',
        hovertemplate='<b>%{text}</b><br>Avg Price: $%{x:.2f}<br>Total Qty: %{y}<extra></extra>'
    ))
    
    fig.update_layout(
        xaxis=dict(title='Average Unit Price ($)'),
        yaxis=dict(title='Total Quantity Sold'),
        showlegend=False,
        annotations=[
            dict(
                x=avg_price * 1.5,
                y=avg_qty * 1.5,
                text="High Price<br>High Volume",
                showarrow=False,
                font=dict(size=10, color='gray')
            ),
            dict(
                x=avg_price * 0.5,
                y=avg_qty * 1.5,
                text="Low Price<br>High Volume",
                showarrow=False,
                font=dict(size=10, color='gray')
            ),
            dict(
                x=avg_price * 1.5,
                y=avg_qty * 0.5,
                text="High Price<br>Low Volume",
                showarrow=False,
                font=dict(size=10, color='gray')
            ),
            dict(
                x=avg_price * 0.5,
                y=avg_qty * 0.5,
                text="Low Price<br>Low Volume",
                showarrow=False,
                font=dict(size=10, color='gray')
            )
        ]
    )
    
    fig = style_chart(fig, title="Category Analysis: Price vs Quantity Quadrants", height=450)
    
    return dcc.Graph(figure=fig, config={'displayModeBar': False})

def create_top_products_detailed(df, n=15):
    """
    Create detailed top products bar chart
    """
    
    top_products = (
        df.groupby('product_detail')
        .agg({
            'Total_Bill': 'sum',
            'transaction_qty': 'sum',
            'transaction_id': 'count'
        })
        .sort_values('Total_Bill', ascending=True)
        .tail(n)
        .reset_index()
    )
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        y=top_products['product_detail'],
        x=top_products['Total_Bill'],
        orientation='h',
        marker=dict(
            color=top_products['Total_Bill'],
            colorscale='Burg',
            showscale=False
        ),
        text=top_products['Total_Bill'],
        texttemplate='$%{text:.2s}',
        textposition='outside',
        hovertemplate='<b>%{y}</b><br>Revenue: $%{x:,.2f}<br>Qty: %{customdata[0]}<br>Transactions: %{customdata[1]}<extra></extra>',
        customdata=top_products[['transaction_qty', 'transaction_id']]
    ))
    
    fig.update_layout(
        yaxis=dict(tickfont=dict(size=10)),
        xaxis=dict(title='Revenue ($)'),
        showlegend=False
    )
    
    fig = style_chart(fig, title=f"Top {n} Products by Revenue", height=500)
    
    return dcc.Graph(figure=fig, config={'displayModeBar': False})

def create_time_distribution(df):
    """
    Create distribution plot for sales over time
    """
    
    stores = df['store_location'].unique()
    hist_data = [df[df['store_location'] == store]['Hour'].tolist() for store in stores]
    group_labels = list(stores)
    
    colors = ['#2ca02c', '#ff7f0e', '#1f77b4', '#d62728', '#9467bd'][:len(stores)]
    
    fig = ff.create_distplot(
        hist_data,
        group_labels,
        bin_size=1,
        colors=colors,
        show_rug=True,
        show_hist=True
    )
    
    fig.update_layout(
        xaxis=dict(title='Hour of Day', range=[6, 21]),
        yaxis=dict(title='Density'),
        legend=dict(title='Store Location')
    )
    
    fig = style_chart(fig, title="Sales Distribution by Hour (All Stores)", height=450)
    
    return dcc.Graph(figure=fig, config={'displayModeBar': False})

def create_ticket_distribution(df):
    """
    Create distribution plot for ticket amounts by store
    """
    
    stores = df['store_location'].unique()
    hist_data = [df[df['store_location'] == loc]['Total_Bill'].dropna().tolist() for loc in stores]
    group_labels = list(stores)
    
    colors = ['#2ca02c', '#ff7f0e', '#1f77b4', '#d62728', '#9467bd'][:len(stores)]
    
    fig = ff.create_distplot(
        hist_data,
        group_labels,
        bin_size=0.5,
        colors=colors,
        curve_type='kde',
        show_hist=True,
        show_rug=True
    )
    
    fig.update_layout(
        xaxis=dict(title='Ticket Amount ($)'),
        yaxis=dict(title='Density'),
        legend=dict(title='Store Location')
    )
    
    fig = style_chart(fig, title="Ticket Amount Distribution by Store", height=450)
    
    return dcc.Graph(figure=fig, config={'displayModeBar': False})

def create_day_distribution(df):
    """
    Create distribution plot for sales concentration by day of month
    """
    
    stores = df['store_location'].unique()
    hist_data = [df[df['store_location'] == store]['Day'].tolist() for store in stores]
    group_labels = list(stores)
    
    colors = ['#2ca02c', '#ff7f0e', '#1f77b4', '#d62728', '#9467bd'][:len(stores)]
    
    fig = ff.create_distplot(
        hist_data,
        group_labels,
        bin_size=1,
        colors=colors,
        show_rug=True
    )
    
    fig.update_layout(
        xaxis=dict(title='Day of Month', range=[1, 31], dtick=5),
        yaxis=dict(title='Density'),
        legend=dict(title='Store Location')
    )
    
    fig = style_chart(fig, title="Sales Concentration by Day of Month", height=450)
    
    return dcc.Graph(figure=fig, config={'displayModeBar': False})

def create_temporal_evolution(df):
    """
    Create temporal evolution chart with dual y-axis
    """
    
    temporal_df = df.groupby('Day').agg({
        'Total_Bill': 'sum',
        'transaction_qty': 'sum',
        'transaction_id': 'nunique'
    }).reset_index()
    
    temporal_df['avg_ticket'] = temporal_df['Total_Bill'] / temporal_df['transaction_id']
    
    fig = go.Figure()
    
    # Total sales (primary y-axis)
    fig.add_trace(go.Scatter(
        x=temporal_df['Day'],
        y=temporal_df['Total_Bill'],
        mode='lines+markers',
        name='Total Sales ($)',
        line=dict(color='#59270E', width=3),
        marker=dict(size=8),
        yaxis='y'
    ))
    
    # Average ticket (secondary y-axis)
    fig.add_trace(go.Scatter(
        x=temporal_df['Day'],
        y=temporal_df['avg_ticket'],
        mode='lines',
        name='Avg Ticket ($)',
        line=dict(color='#4682B4', width=2, dash='dot'),
        yaxis='y2'
    ))
    
    fig.update_layout(
        xaxis=dict(
            title='Day of Month',
            tickmode='linear',
            range=[1, 31]
        ),
        yaxis=dict(
            title=dict(text='Total Sales ($)', font=dict(color='#59270E')),
            tickfont=dict(color='#59270E')
        ),
        yaxis2=dict(
            title=dict(text='Average Ticket ($)', font=dict(color='#4682B4')),
            tickfont=dict(color='#4682B4'),
            anchor='x',
            overlaying='y',
            side='right'
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.05,
            xanchor="center",
            x=0.5
        )
    )
    
    fig = style_chart(fig, title="Daily Sales & Average Ticket Evolution", height=450)
    
    return dcc.Graph(figure=fig, config={'displayModeBar': False})



