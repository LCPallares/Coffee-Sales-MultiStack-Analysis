"""
Theme configuration for the dashboard
"""

def get_theme():
    """
    Returns the Mantine theme configuration with custom styling
    inspired by coffee shop aesthetics
    """
    
    return {
        "colorScheme": "light",
        "primaryColor": "brown",
        "colors": {
            "brown": [
                "#F5E6D3",  # 0 - Cream
                "#E8D4BB",  # 1 - Light tan
                "#D4B896",  # 2 - Tan
                "#C09F76",  # 3 - Light coffee
                "#A67C52",  # 4 - Medium coffee
                "#8B4513",  # 5 - Coffee brown (primary)
                "#6F3609",  # 6 - Dark coffee
                "#5C2D08",  # 7 - Espresso
                "#4A2507",  # 8 - Dark espresso
                "#3A1E06",  # 9 - Almost black
            ]
        },
        "fontFamily": "'Space Mono', monospace",
        "headings": {
            "fontFamily": "'Playfair Display', serif",
            "fontWeight": "700"
        },
        "defaultRadius": "md",
        "components": {
            "Paper": {
                "styles": {
                    "root": {
                        "transition": "all 0.3s ease",
                        "&:hover": {
                            "transform": "translateY(-2px)",
                            "boxShadow": "0 4px 12px rgba(0,0,0,0.1)"
                        }
                    }
                }
            },
            "Button": {
                "styles": {
                    "root": {
                        "fontFamily": "'Space Mono', monospace",
                        "fontWeight": "700"
                    }
                }
            }
        }
    }

# Plotly chart theme
CHART_COLORS = {
    "primary": "#8B4513",
    "secondary": "#D4B896",
    "accent": "#C09F76",
    "success": "#52C41A",
    "warning": "#FAAD14",
    "danger": "#F5222D",
    "info": "#1890FF",
    "background": "#FAFAFA",
    "text": "#2C1810"
}

CHART_TEMPLATE = {
    "layout": {
        "font": {
            "family": "Space Mono, monospace",
            "color": CHART_COLORS["text"]
        },
        "paper_bgcolor": "rgba(0,0,0,0)",
        "plot_bgcolor": "rgba(0,0,0,0)",
        "colorway": [
            "#8B4513", "#D4B896", "#C09F76", "#A67C52",
            "#6F3609", "#E8D4BB", "#F5E6D3", "#5C2D08"
        ],
        "title": {
            "font": {
                "family": "Playfair Display, serif",
                "size": 20,
                "color": CHART_COLORS["text"]
            }
        },
        "xaxis": {
            "gridcolor": "#E5E5E5",
            "linecolor": "#D4D4D4",
            "zerolinecolor": "#D4D4D4"
        },
        "yaxis": {
            "gridcolor": "#E5E5E5",
            "linecolor": "#D4D4D4",
            "zerolinecolor": "#D4D4D4"
        }
    }
}

def style_chart(fig, title=None, height=400):
    """
    Apply consistent styling to Plotly figures
    
    Parameters:
    -----------
    fig : plotly.graph_objects.Figure
        The figure to style
    title : str, optional
        Chart title
    height : int, optional
        Chart height in pixels
    """
    
    fig.update_layout(
        template=CHART_TEMPLATE,
        height=height,
        margin=dict(l=40, r=40, t=60, b=40),
        hovermode='x unified',
        hoverlabel=dict(
            bgcolor="white",
            font_size=12,
            font_family="Space Mono, monospace"
        )
    )
    
    if title:
        fig.update_layout(
            title={
                "text": title,
                "font": {
                    "family": "Playfair Display, serif",
                    "size": 20,
                    "color": CHART_COLORS["text"]
                },
                "x": 0,
                "xanchor": "left"
            }
        )
    
    return fig
