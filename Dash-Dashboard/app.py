import dash
from dash import dcc, html, dash_table, Input, Output, callback
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import os

# --- CARGA Y PROCESAMIENTO DE DATOS ---
def load_data():
    # Ajusta la ruta según tu estructura de carpetas
    base_path = os.path.dirname(__file__)
    #file_path = os.path.join(base_path, "coffee_shop_sales.csv") # Simplificado para el ejemplo
    file_path = os.path.join(base_path, "..", "Data", "coffee_shop_sales.csv")
    
    if not os.path.exists(file_path):
        # Datos de prueba en caso de que no encuentre el archivo local
        df = pd.DataFrame() 
        return df

    df = pd.read_csv(file_path)
    df['transaction_date'] = pd.to_datetime(df['transaction_date'], dayfirst=True)
    df['Month_Name'] = df['transaction_date'].dt.month_name()
    df['Day'] = df['transaction_date'].dt.day
    df['Day Name'] = df['transaction_date'].dt.day_name()
    df['Total_Bill'] = df['unit_price'] * df['transaction_qty']
    return df

df_master = load_data()
meses_lista = ["January", "February", "March", "April", "May", "June"]

# --- APP INITIALIZATION ---
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUX])

# --- STYLES ---
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#3d2b1f",
    "color": "white"
}

CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
    "background-color": "#fdf5e6"
}

# --- LAYOUT COMPONENTS ---
sidebar = html.Div(
    [
        html.H2("Coffee Dash", className="display-6"),
        html.Hr(),
        html.P("Navegación:", className="lead"),
        dbc.Nav(
            [
                dbc.NavLink("Overview", href="/", active="exact"),
                dbc.NavLink("Monthly Sales", href="/monthly", active="exact"),
                dbc.NavLink("Shopper Behavior", href="/behavior", active="exact"),
                dbc.NavLink("Advanced Analytics", href="/advanced", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
        html.Hr(),
        html.P("Filtro de Mes:"),
        dcc.Dropdown(
            id='month-filter',
            options=[{'label': 'Todas', 'value': 'Todas'}] + [{'label': m, 'value': m} for m in meses_lista],
            value='Todas',
            style={'color': 'black'}
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", style=CONTENT_STYLE)

app.layout = html.Div([dcc.Location(id="url"), sidebar, content])

# --- CALLBACKS PARA NAVEGACIÓN ---
@app.callback(Output("page-content", "children"), 
              [Input("url", "pathname"), Input("month-filter", "value")])
def render_page_content(pathname, mes_seleccionado):
    # Filtrado de datos
    df = df_master.copy()
    if mes_seleccionado != "Todas":
        df = df[df['Month_Name'] == mes_seleccionado]

    if pathname == "/":
        return layout_overview(df)
    elif pathname == "/monthly":
        return layout_monthly(df, mes_seleccionado)
    elif pathname == "/behavior":
        return layout_behavior(df)
    elif pathname == "/advanced":
        return layout_advanced(df_master)
    return html.Div([html.H1("404: Not found")], className="p-3")

# --- FUNCIONES DE LAYOUT (EQUIVALENTES A TUS FUNCIONES EN STREAMLIT) ---

def create_kpi_cards(df_filtered):
    v_act = df_filtered['Total_Bill'].sum()
    q_act = df_filtered['transaction_qty'].sum()
    t_act = df_filtered['transaction_id'].nunique()
    
    return dbc.Row([
        dbc.Col(dbc.Card(dbc.CardBody([html.H5("Ventas Totales"), html.H3(f"${v_act:,.2f}")]), color="white")),
        dbc.Col(dbc.Card(dbc.CardBody([html.H5("Cantidad Vendida"), html.H3(f"{q_act:,}")]), color="white")),
        dbc.Col(dbc.Card(dbc.CardBody([html.H5("Total Transacciones"), html.H3(f"{t_act:,}")]), color="white")),
    ], className="mb-4")

def layout_overview(df):
    # Gráfico de Categorías
    cat_data = df.groupby('product_category')['Total_Bill'].sum().sort_values(ascending=True).reset_index()
    fig_cat = px.bar(cat_data, x='Total_Bill', y='product_category', orientation='h', 
                     color_discrete_sequence=['#6f4e37'], template="simple_white")

    # Gráfico de Tiendas
    fig_pie = px.pie(df, values='Total_Bill', names='store_location', hole=0.5,
                     color_discrete_sequence=['#3d2b1f', '#6f4e37', '#c3a689'])

    return html.Div([
        html.H1("📊 Coffee Overview"),
        create_kpi_cards(df),
        dbc.Row([
            dbc.Col(dcc.Graph(figure=fig_cat), width=7),
            dbc.Col(dcc.Graph(figure=fig_pie), width=5),
        ]),
        html.Hr(),
        html.H3("Resumen de Categorías"),
        dash_table.DataTable(
            data=df.groupby('product_category')['Total_Bill'].sum().reset_index().to_dict('records'),
            columns=[{"name": i, "id": i} for i in ['product_category', 'Total_Bill']],
            style_table={'overflowX': 'auto'},
            style_cell={'textAlign': 'left', 'padding': '10px'},
            style_header={'backgroundColor': '#3d2b1f', 'color': 'white'}
        )
    ])

def layout_monthly(df, mes):
    if mes == "Todas":
        return html.Div([dbc.Alert("Selecciona un mes en el menú lateral para ver el detalle.", color="warning")])
    
    # Simulación de tendencia diaria
    daily = df.groupby('Day')['Total_Bill'].sum().reset_index()
    fig_daily = px.bar(daily, x='Day', y='Total_Bill', color_discrete_sequence=['#59270E'], template="simple_white")
    
    return html.Div([
        html.H1(f"📈 Análisis Detallado: {mes}"),
        create_kpi_cards(df),
        dcc.Graph(figure=fig_daily)
    ])

def layout_behavior(df):
    # Heatmap simplificado
    orden_dias = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    pivot = df.pivot_table(index='Hour', columns='Day Name', values='Total_Bill', aggfunc='sum').reindex(columns=orden_dias).fillna(0)
    fig_heat = px.imshow(pivot, color_continuous_scale=[[0, '#fdf5e6'], [1, '#59270E']])
    
    return html.Div([
        html.H1("👥 Comportamiento del Consumidor"),
        dcc.Graph(figure=fig_heat),
        html.H3("Matriz Estratégica"),
        # Aquí podrías añadir el gráfico de burbujas que tienes en Streamlit
    ])

def layout_advanced(df_full):
    # Gráfico de áreas temporal
    df_temporal = df_full.groupby(['transaction_date', 'store_location'])['Total_Bill'].sum().reset_index()
    fig_area = px.area(df_temporal, x="transaction_date", y="Total_Bill", color="store_location",
                       color_discrete_sequence=['#3d2b1f', '#6f4e37', '#c3a689'], template="simple_white")
    
    return html.Div([
        html.H1("Advanced Analytics"),
        dcc.Graph(figure=fig_area)
    ])

if __name__ == '__main__':
    app.run(debug=True)