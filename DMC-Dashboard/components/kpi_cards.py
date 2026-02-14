"""
KPI Cards component
"""

import dash_mantine_components as dmc
from dash import html
from dash_iconify import DashIconify
from utils.data_loader import calculate_metrics

def create_kpi_cards(df):
    """
    Create KPI cards showing key business metrics
    
    Parameters:
    -----------
    df : pd.DataFrame
        Filtered dataframe
        
    Returns:
    --------
    dmc.Grid
        Grid containing KPI cards
    """
    
    metrics = calculate_metrics(df)
    
    cards = [
        {
            "title": "Total Revenue",
            "value": f"${metrics['total_revenue']:,.2f}",
            "icon": "tabler:currency-dollar",
            "color": "brown",
            "trend": metrics['revenue_growth'],
            "trend_label": "vs previous period"
        },
        {
            "title": "Transactions",
            "value": f"{metrics['total_transactions']:,}",
            "icon": "tabler:shopping-cart",
            "color": "teal",
            "trend": metrics['transaction_growth'],
            "trend_label": "vs previous period"
        },
        {
            "title": "Avg Transaction",
            "value": f"${metrics['avg_transaction']:.2f}",
            "icon": "tabler:receipt",
            "color": "orange",
            "trend": None,
            "trend_label": "per transaction"
        },
        {
            "title": "Items Sold",
            "value": f"{metrics['total_quantity']:,}",
            "icon": "tabler:package",
            "color": "blue",
            "trend": None,
            "trend_label": f"Avg {metrics['avg_items_per_transaction']:.1f} per order"
        }
    ]
    
    return dmc.Grid(
        gutter="md",
        children=[
            dmc.GridCol(
                span={"base": 12, "xs": 6, "md": 3},
                children=create_kpi_card(**card)
            )
            for card in cards
        ]
    )

def create_kpi_card(title, value, icon, color, trend=None, trend_label=""):
    """
    Create a single KPI card
    
    Parameters:
    -----------
    title : str
        Card title
    value : str
        Main metric value
    icon : str
        Iconify icon name
    color : str
        Mantine color
    trend : float, optional
        Trend percentage
    trend_label : str
        Label for trend or additional info
        
    Returns:
    --------
    dmc.Paper
        Styled KPI card
    """
    
    # Determine trend color and icon
    trend_color = "green" if trend and trend > 0 else "red" if trend and trend < 0 else "gray"
    trend_icon = "tabler:trending-up" if trend and trend > 0 else "tabler:trending-down" if trend and trend < 0 else None
    
    return dmc.Paper(
        shadow="sm",
        p="lg",
        withBorder=True,
        style={
            "height": "100%",
            "background": "linear-gradient(135deg, #FFFFFF 0%, #FAF7F2 100%)",
            "borderLeft": f"4px solid var(--mantine-color-{color}-5)"
        },
        children=dmc.Stack(
            gap="xs",
            children=[
                # Header with icon
                dmc.Group(
                    justify="space-between",
                    align="flex-start",
                    children=[
                        dmc.Text(
                            title,
                            size="sm",
                            c="dimmed",
                            fw=600,
                            style={
                                "fontFamily": "Space Mono, monospace",
                                "textTransform": "uppercase",
                                "letterSpacing": "0.05em"
                            }
                        ),
                        dmc.ThemeIcon(
                            DashIconify(icon=icon, width=20),
                            variant="light",
                            color=color,
                            size="lg",
                            radius="md"
                        )
                    ]
                ),
                
                # Main value
                dmc.Text(
                    value,
                    style={
                        "fontSize": "28px",
                        "fontWeight": 700,
                        "fontFamily": "Playfair Display, serif",
                        "color": "#2C1810",
                        "lineHeight": 1.2
                    }
                ),
                
                # Trend indicator
                dmc.Group(
                    gap="xs",
                    mt="xs",
                    children=[
                        DashIconify(
                            icon=trend_icon,
                            width=16,
                            color=f"var(--mantine-color-{trend_color}-6)"
                        ) if trend_icon else None,
                        dmc.Text(
                            f"{abs(trend):.1f}%" if trend is not None else "",
                            size="sm",
                            c=trend_color,
                            fw=600,
                            style={"fontFamily": "Space Mono, monospace"}
                        ) if trend is not None else None,
                        dmc.Text(
                            trend_label,
                            size="xs",
                            c="dimmed",
                            style={"fontFamily": "Space Mono, monospace"}
                        )
                    ]
                )
            ]
        )
    )
