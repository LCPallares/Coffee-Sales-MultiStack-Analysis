"""
Coffee Shop Sales Dashboard
A modular, scalable dashboard built with Dash and Dash Mantine Components
"""

import dash
from dash import Dash, html, dcc, Input, Output, State, callback
import dash_mantine_components as dmc
from dash_iconify import DashIconify
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# Import modular components
from components.filters import create_filters
from components.kpi_cards import create_kpi_cards
from components.charts import (
    create_sales_trend,
    create_category_distribution,
    create_hourly_heatmap,
    create_top_products,
    create_store_comparison,
    create_weekday_analysis,

    create_size_distribution,  # ← NUEVO

    # New charts from Streamlit
    create_monthly_trend,
    create_daily_sales_bar,
    create_category_comparison,
    create_category_variation,
    create_heatmap_with_totals,
    create_price_transaction_analysis,
    create_category_price_qty_quadrants,
    create_top_products_detailed,
    create_time_distribution,
    create_ticket_distribution,
    create_day_distribution,
    create_temporal_evolution
)
from utils.data_loader import load_and_prepare_data
from utils.theme import get_theme

# Initialize the Dash app
app = Dash(
    __name__,
    suppress_callback_exceptions=True,
    external_stylesheets=[
        "https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=Space+Mono:wght@400;700&display=swap"
    ]
)

# Load data
df = load_and_prepare_data('../Data/coffee_shop_sales.csv')

# App layout
app.layout = dmc.MantineProvider(
    theme=get_theme(),
    children=dmc.AppShell(
        children=[
            # Header
            dmc.AppShellHeader(
                children=dmc.Container(
                    size="xl",
                    children=dmc.Group(
                        justify="space-between",
                        align="center",
                        style={"height": "70px"},
                        children=[
                            dmc.Group(
                                gap="md",
                                children=[
                                    DashIconify(
                                        icon="tabler:coffee",
                                        width=40,
                                        color="#8B4513"
                                    ),
                                    dmc.Stack(
                                        gap=0,
                                        children=[
                                            dmc.Title(
                                                "Coffee Analytics",
                                                order=2,
                                                style={
                                                    "fontFamily": "Playfair Display, serif",
                                                    "fontWeight": 700,
                                                    "color": "#2C1810",
                                                    "letterSpacing": "-0.02em"
                                                }
                                            ),
                                            dmc.Text(
                                                "Sales Performance Dashboard",
                                                size="xs",
                                                c="dimmed",
                                                style={"fontFamily": "Space Mono, monospace"}
                                            )
                                        ]
                                    )
                                ]
                            ),
                            dmc.Group(
                                gap="xs",
                                children=[
                                    dmc.Badge(
                                        "Live Data",
                                        variant="dot",
                                        color="green",
                                        size="lg"
                                    ),
                                    dmc.ActionIcon(
                                        DashIconify(icon="tabler:refresh", width=20),
                                        variant="subtle",
                                        size="lg",
                                        id="refresh-button"
                                    )
                                ]
                            )
                        ]
                    )
                )
            ),
            
            # Main content
            dmc.AppShellMain(
                children=dmc.Container(
                    size="xl",
                    pt="md",
                    pb="xl",
                    children=[
                        # Filters section
                        dmc.Paper(
                            shadow="xs",
                            p="md",
                            mb="lg",
                            withBorder=True,
                            style={"backgroundColor": "#FAF7F2"},
                            children=create_filters(df)
                        ),
                        
                        # KPI Cards
                        html.Div(id="kpi-cards", children=create_kpi_cards(df)),
                        
                        # Charts Grid
                        dmc.Grid(
                            gutter="lg",
                            mt="lg",
                            children=[
                                # Sales Trend
                                dmc.GridCol(
                                    span=12,
                                    children=dmc.Paper(
                                        shadow="sm",
                                        p="md",
                                        withBorder=True,
                                        children=html.Div(id="sales-trend-chart")
                                    )
                                ),
                                
                                # Category Distribution & Top Products
                                dmc.GridCol(
                                    span={"base": 12, "md": 6},
                                    children=dmc.Paper(
                                        shadow="sm",
                                        p="md",
                                        withBorder=True,
                                        children=html.Div(id="category-chart")
                                    )
                                ),
                                dmc.GridCol(
                                    span={"base": 12, "md": 6},
                                    children=dmc.Paper(
                                        shadow="sm",
                                        p="md",
                                        withBorder=True,
                                        children=html.Div(id="top-products-chart")
                                    )
                                ),
                                
                                # Hourly Heatmap
                                dmc.GridCol(
                                    span=12,
                                    children=dmc.Paper(
                                        shadow="sm",
                                        p="md",
                                        withBorder=True,
                                        children=html.Div(id="heatmap-chart")
                                    )
                                ),
                                
                                # Store Comparison & Weekday Analysis
                                dmc.GridCol(
                                    span={"base": 12, "md": 6},
                                    children=dmc.Paper(
                                        shadow="sm",
                                        p="md",
                                        withBorder=True,
                                        children=html.Div(id="store-chart")
                                    )
                                ),
                                dmc.GridCol(
                                    span={"base": 12, "md": 6},
                                    children=dmc.Paper(
                                        shadow="sm",
                                        p="md",
                                        withBorder=True,
                                        children=html.Div(id="weekday-chart")
                                    )
                                ),

                                dmc.GridCol(
                                    span={"base": 12, "md": 6},
                                    children=dmc.Paper(
                                        shadow="sm",
                                        p="md",
                                        withBorder=True,
                                        children=html.Div(id="size-chart")
                                    )
                                ),

                                # from streamlit charts

                                dmc.GridCol(
                                    span={"base": 12, "md": 6},
                                    children=dmc.Paper(
                                        shadow="sm",
                                        p="md",
                                        withBorder=True,
                                        children=html.Div(id="monthly_trend")
                                    )
                                ),
                                dmc.GridCol(
                                    span={"base": 12, "md": 6},
                                    children=dmc.Paper(
                                        shadow="sm",
                                        p="md",
                                        withBorder=True,
                                        children=html.Div(id="daily_sales_bar")
                                    )
                                ),

                                # dmc.GridCol(
                                #     span={"base": 12, "md": 6},
                                #     children=dmc.Paper(
                                #         shadow="sm",
                                #         p="md",
                                #         withBorder=True,
                                #         children=html.Div(id="category_comparison")
                                #     )
                                # ),
                                # dmc.GridCol(
                                #     span={"base": 12, "md": 6},
                                #     children=dmc.Paper(
                                #         shadow="sm",
                                #         p="md",
                                #         withBorder=True,
                                #         children=html.Div(id="category_variation")
                                #     )
                                # ),

                                dmc.GridCol(
                                    span={"base": 12, "md": 6},
                                    children=dmc.Paper(
                                        shadow="sm",
                                        p="md",
                                        withBorder=True,
                                        children=html.Div(id="heatmap_with_totals")
                                    )
                                ),
                                dmc.GridCol(
                                    span={"base": 12, "md": 6},
                                    children=dmc.Paper(
                                        shadow="sm",
                                        p="md",
                                        withBorder=True,
                                        children=html.Div(id="price_transaction_analysis")
                                    )
                                ),

                                dmc.GridCol(
                                    span={"base": 12, "md": 6},
                                    children=dmc.Paper(
                                        shadow="sm",
                                        p="md",
                                        withBorder=True,
                                        children=html.Div(id="category_price_qty_quadrants")
                                    )
                                ),
                                dmc.GridCol(
                                    span={"base": 12, "md": 6},
                                    children=dmc.Paper(
                                        shadow="sm",
                                        p="md",
                                        withBorder=True,
                                        children=html.Div(id="top_products_detailed")
                                    )
                                ),

                                dmc.GridCol(
                                    span={"base": 12, "md": 6},
                                    children=dmc.Paper(
                                        shadow="sm",
                                        p="md",
                                        withBorder=True,
                                        children=html.Div(id="time_distribution")
                                    )
                                ),
                                dmc.GridCol(
                                    span={"base": 12, "md": 6},
                                    children=dmc.Paper(
                                        shadow="sm",
                                        p="md",
                                        withBorder=True,
                                        children=html.Div(id="ticket_distribution")
                                    )
                                ),

                                dmc.GridCol(
                                    span={"base": 12, "md": 6},
                                    children=dmc.Paper(
                                        shadow="sm",
                                        p="md",
                                        withBorder=True,
                                        children=html.Div(id="day_distribution")
                                    )
                                ),
                                dmc.GridCol(
                                    span={"base": 12, "md": 6},
                                    children=dmc.Paper(
                                        shadow="sm",
                                        p="md",
                                        withBorder=True,
                                        children=html.Div(id="temporal_evolution")
                                    )
                                )



                            ]
                        )
                    ]
                )
            )
        ],
        header={"height": 70}
    )
)

# Callbacks
@callback(
    [
        Output("kpi-cards", "children"),
        Output("sales-trend-chart", "children"),
        Output("category-chart", "children"),
        Output("top-products-chart", "children"),
        Output("heatmap-chart", "children"),
        Output("store-chart", "children"),
        Output("weekday-chart", "children"),

        Output("size-chart", "children"),  # ← NUEVO

        Output("monthly_trend", "children"),
        Output("daily_sales_bar", "children"),
        # Output("category_comparison", "children"),
        # Output("category_variation", "children"),
        Output("heatmap_with_totals", "children"),
        Output("price_transaction_analysis", "children"),
        Output("category_price_qty_quadrants", "children"),
        Output("top_products_detailed", "children"),
        Output("time_distribution", "children"),
        Output("ticket_distribution", "children"),
        Output("day_distribution", "children"),
        Output("temporal_evolution", "children")

    ],
    [
        Input("date-range", "value"),
        Input("month-filter", "value"),
        Input("store-filter", "value"),
        Input("category-filter", "value"),
        Input("product-filter", "value")
    ]
)
def update_dashboard(date_range, months, stores, categories, products):
    """Update all dashboard components based on filters"""
    
    # Filter data
    filtered_df = df.copy()
    
    if date_range:
        start_date = pd.to_datetime(date_range[0])
        end_date = pd.to_datetime(date_range[1])
        filtered_df = filtered_df[
            (filtered_df['transaction_date'] >= start_date) &
            (filtered_df['transaction_date'] <= end_date)
        ]
    
    if months:
        filtered_df = filtered_df[filtered_df['Month Name'].isin(months)]
    
    if stores:
        filtered_df = filtered_df[filtered_df['store_location'].isin(stores)]
    
    if categories:
        filtered_df = filtered_df[filtered_df['product_category'].isin(categories)]
    
    if products:
        filtered_df = filtered_df[filtered_df['product_detail'].isin(products)]
    
    # Generate all components with filtered data
    return (
        create_kpi_cards(filtered_df),
        create_sales_trend(filtered_df),
        create_category_distribution(filtered_df),
        create_top_products(filtered_df),
        create_hourly_heatmap(filtered_df),
        create_store_comparison(filtered_df),
        create_weekday_analysis(filtered_df),

        create_size_distribution(filtered_df),  # ← NUEVO

        create_monthly_trend(filtered_df),
        create_daily_sales_bar(filtered_df),
        # create_category_comparison(filtered_df),
        # create_category_variation(filtered_df),
        create_heatmap_with_totals(filtered_df),
        create_price_transaction_analysis(filtered_df),
        create_category_price_qty_quadrants(filtered_df),
        create_top_products_detailed(filtered_df),
        create_time_distribution(filtered_df),
        create_ticket_distribution(filtered_df),
        create_day_distribution(filtered_df),
        create_temporal_evolution(filtered_df)

    )

if __name__ == '__main__':
    app.run(debug=True, port=8050)
