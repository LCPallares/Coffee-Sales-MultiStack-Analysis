"""
Filter components for the dashboard
"""

import dash_mantine_components as dmc
from dash import html
from dash_iconify import DashIconify
import pandas as pd

def create_filters(df):
    """
    Create the filters section with all filter controls
    
    Parameters:
    -----------
    df : pd.DataFrame
        The full dataframe to extract filter options from
        
    Returns:
    --------
    dmc.Stack
        Stack containing all filter components
    """
    
    # Get filter options
    stores = sorted(df['store_location'].unique().tolist())
    categories = sorted(df['product_category'].unique().tolist())
    products = sorted(df['product_detail'].unique().tolist())
    
    # Get date range
    min_date = df['transaction_date'].min()
    max_date = df['transaction_date'].max()
    
    return dmc.Stack(
        gap="md",
        children=[
            # Title and description
            dmc.Group(
                justify="space-between",
                align="center",
                children=[
                    dmc.Stack(
                        gap=0,
                        children=[
                            dmc.Title(
                                "Filters",
                                order=4,
                                style={
                                    "fontFamily": "Playfair Display, serif",
                                    "color": "#2C1810"
                                }
                            ),
                            dmc.Text(
                                "Customize your view by selecting filters below",
                                size="sm",
                                c="dimmed",
                                style={"fontFamily": "Space Mono, monospace"}
                            )
                        ]
                    ),
                    dmc.Button(
                        "Reset Filters",
                        leftSection=DashIconify(icon="tabler:refresh", width=16),
                        variant="light",
                        color="brown",
                        size="sm",
                        id="reset-filters-btn"
                    )
                ]
            ),
            
            dmc.Divider(variant="dashed"),
            
            # Filter controls
            dmc.Grid(
                gutter="md",
                children=[
                    # Date Range
                    dmc.GridCol(
                        span={"base": 12, "sm": 6, "md": 3},
                        children=dmc.Stack(
                            gap="xs",
                            children=[
                                dmc.Group(
                                    gap="xs",
                                    children=[
                                        DashIconify(
                                            icon="tabler:calendar",
                                            width=18,
                                            color="#8B4513"
                                        ),
                                        dmc.Text(
                                            "Date Range",
                                            size="sm",
                                            fw=600,
                                            style={"fontFamily": "Space Mono, monospace"}
                                        )
                                    ]
                                ),
                                dmc.DatePicker(
                                    id="date-range",
                                    type="range",
                                    value=[
                                        min_date.strftime('%Y-%m-%d'),
                                        max_date.strftime('%Y-%m-%d')
                                    ],
                                    minDate=min_date.strftime('%Y-%m-%d'),
                                    maxDate=max_date.strftime('%Y-%m-%d'),
                                    style={"width": "100%"}
                                )
                            ]
                        )
                    ),
                    
                    # Store Filter
                    dmc.GridCol(
                        span={"base": 12, "sm": 6, "md": 3},
                        children=dmc.Stack(
                            gap="xs",
                            children=[
                                dmc.Group(
                                    gap="xs",
                                    children=[
                                        DashIconify(
                                            icon="tabler:building-store",
                                            width=18,
                                            color="#8B4513"
                                        ),
                                        dmc.Text(
                                            "Store Location",
                                            size="sm",
                                            fw=600,
                                            style={"fontFamily": "Space Mono, monospace"}
                                        )
                                    ]
                                ),
                                dmc.MultiSelect(
                                    id="store-filter",
                                    data=stores,
                                    placeholder="All stores",
                                    searchable=True,
                                    clearable=True,
                                    leftSection=DashIconify(icon="tabler:map-pin", width=16),
                                    style={"width": "100%"}
                                )
                            ]
                        )
                    ),
                    
                    # Category Filter
                    dmc.GridCol(
                        span={"base": 12, "sm": 6, "md": 3},
                        children=dmc.Stack(
                            gap="xs",
                            children=[
                                dmc.Group(
                                    gap="xs",
                                    children=[
                                        DashIconify(
                                            icon="tabler:category",
                                            width=18,
                                            color="#8B4513"
                                        ),
                                        dmc.Text(
                                            "Product Category",
                                            size="sm",
                                            fw=600,
                                            style={"fontFamily": "Space Mono, monospace"}
                                        )
                                    ]
                                ),
                                dmc.MultiSelect(
                                    id="category-filter",
                                    data=categories,
                                    placeholder="All categories",
                                    searchable=True,
                                    clearable=True,
                                    leftSection=DashIconify(icon="tabler:tag", width=16),
                                    style={"width": "100%"}
                                )
                            ]
                        )
                    ),
                    
                    # Product Filter
                    dmc.GridCol(
                        span={"base": 12, "sm": 6, "md": 3},
                        children=dmc.Stack(
                            gap="xs",
                            children=[
                                dmc.Group(
                                    gap="xs",
                                    children=[
                                        DashIconify(
                                            icon="tabler:cup",
                                            width=18,
                                            color="#8B4513"
                                        ),
                                        dmc.Text(
                                            "Product",
                                            size="sm",
                                            fw=600,
                                            style={"fontFamily": "Space Mono, monospace"}
                                        )
                                    ]
                                ),
                                dmc.MultiSelect(
                                    id="product-filter",
                                    data=products,
                                    placeholder="All products",
                                    searchable=True,
                                    clearable=True,
                                    leftSection=DashIconify(icon="tabler:coffee", width=16),
                                    style={"width": "100%"},
                                    maxDropdownHeight=300
                                )
                            ]
                        )
                    )
                ]
            )
        ]
    )
