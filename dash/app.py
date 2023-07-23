import json

import dash
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
from dash import dash_table
import colorlover as cl

# Cargar los datos que se quieren graficar
df_2019 = pd.read_csv("C:/Users/laptop/Documents/Maestria/TFM/proyecto/DB/2019/contratos_por_municipio-sector-grupo_ocupacion-genero-edad-2019.csv", sep=";")

# Dataframe Número de Contratos por provincia en base al Genero
df_contratos_by_genero = df_2019.groupby(['NOM_PROV', 'DESC_GENERO'])['NUM_CONTRATOS'].sum().reset_index(
    name='total_contratos')

# Dataframe Número de Contratos por provincia en base a la Edad
df_contratos_by_edad = df_2019.groupby(['NOM_PROV', 'RANGO_EDAD'])['NUM_CONTRATOS'].sum().reset_index(
    name='total_contratos')

# Dataframe Número de Contratos por provincia en base al Sector
df_contratos_by_sector = df_2019.groupby(['NOM_PROV', 'DESC_SECTOR'])['NUM_CONTRATOS'].sum().reset_index(
    name='total_contratos')

# Dataframe Número de Contratos en base al Grupo
df_contratos_by_grupo = df_2019.groupby(['COD_GRUPO'])['NUM_CONTRATOS'].sum().reset_index(
    name='total_contratos')

# Dataframe Número de Contratos en base al Grupo y la Edad
df_contratos_by_grupo_and_edad = df_2019.groupby(['COD_GRUPO', 'RANGO_EDAD'])['NUM_CONTRATOS'].sum().reset_index(
    name='total_contratos')

# Dataframe Número de Contratos en base al Grupo y el Genero
df_contratos_by_grupo_and_genero = df_2019.groupby(['COD_GRUPO', 'DESC_GENERO'])['NUM_CONTRATOS'].sum().reset_index(
    name='total_contratos')
"""
print(df_contratos_by_grupo)
print(df_contratos_by_grupo_and_edad)
print(df_contratos_by_grupo_and_genero)
"""
# Dataframe Número de Contratos en base al Grupo y el Genero
df_grupos = df_2019[['COD_GRUPO', 'DESC_GRUPO']].drop_duplicates()
df_grupos = df_grupos.sort_values('COD_GRUPO')

# Imprimir los dataframes resultantes
"""
print("NOM_PROV por DESC_GENERO:")
print(df_nom_prov_genero)
print("/nNOM_PROV por EDAD:")
print(df_nom_prov_edad)
print("/nNOM_PROV por DESC_SECTOR:")
print(df_nom_prov_sector)
"""

df_prov = df_2019.drop(columns=['ANYO', 'COD_MUN', 'NOM_MUN', 'COD_SECTOR', 'COD_GRUPO', 'DESC_GRUPO'])
df_prov = df_2019.groupby(['MES', 'COD_PROV', 'NOM_PROV', 'DESC_SECTOR',
                           'DESC_GENERO', 'RANGO_EDAD'], as_index=False)['NUM_CONTRATOS'].sum()

df_prov['COD_PROV'] = df_prov['COD_PROV'].astype(str)
df_prov.loc[df_prov['COD_PROV'] == '3', 'COD_PROV'] = '03'

pd.set_option('display.max_columns', None)

# Para poder graficar en el mapa necesitamos las localizaciones.
with open('C:/Users/laptop/Documents/Maestria/TFM/proyecto/DB/spain-provinces.geojson', 'r', encoding='utf-8') as f:
    geojson = json.load(f)

# Filtrar el geojson para mostrar solo las provincias de Alicante, Castellón y Valencia
provincias = ['03', '12', '46']  # Códigos de las provincias de Alicante, Castellón y Valencia
filtered_geojson = {
    'type': 'FeatureCollection',
    'features': [feature for feature in geojson['features']
                 if feature['properties']['cod_prov'] in provincias]
}

# Crear las opciones para los filtros
options_prov = [{'label': row['NOM_PROV'], 'value': row['NOM_PROV']} for i, row in df_prov.iterrows()]
options_sector = [{'label': row['DESC_SECTOR'], 'value': row['DESC_SECTOR']} for i, row in df_prov.iterrows()]
options_genero = [{'label': row['DESC_GENERO'], 'value': row['DESC_GENERO']} for i, row in df_prov.iterrows()]
options_edad = [{'label': row['RANGO_EDAD'], 'value': row['RANGO_EDAD']} for i, row in df_prov.iterrows()]

# Crear el layout de la aplicación
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SLATE])


def create_bar_chart_genero(df):
    fig = px.bar(df, x='NOM_PROV', y='total_contratos', color='DESC_GENERO', barmode='group',
                 labels={'total_contratos': 'Contratos', 'NOM_PROV': 'Provincia', 'DESC_GENERO': 'Género'})
    fig.update_layout(template='plotly_dark')
    return fig


def create_bar_chart_edad(df):
    fig = px.bar(df, x='NOM_PROV', y='total_contratos', color='RANGO_EDAD', barmode='group',
                 labels={'total_contratos': 'Contratos', 'NOM_PROV': 'Provincia', 'RANGO_EDAD': 'Rango de Edad'})
    fig.update_layout(template='plotly_dark')
    return fig


def create_bar_chart_sector(df):
    fig = px.bar(df, x='NOM_PROV', y='total_contratos', color='DESC_SECTOR', barmode='group',
                 labels={'total_contratos': 'Contratos', 'NOM_PROV': 'Provincia', 'DESC_SECTOR': 'Sector'})
    fig.update_layout(template='plotly_dark')
    return fig


def create_bar_chart_mes(df):
    df_example = df.groupby("MES")["NUM_CONTRATOS"].sum().reset_index()

    month_names = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
                   'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']

    df_example['NOMBRE_MES'] = df_example['MES'].apply(lambda x: month_names[x - 1])

    fig = go.Figure(go.Bar(x=df_example["NOMBRE_MES"], y=df_example["NUM_CONTRATOS"],
                           text=df_example["NUM_CONTRATOS"],
                           textposition='auto'))

    fig.update_layout(
        xaxis_title="Mes",
        yaxis_title="Número de contratos",
        font=dict(color='white'),
        template='plotly_dark'
    )

    return fig


def create_pie_chart():
    df_pie = df_2019.groupby("DESC_SECTOR")["NUM_CONTRATOS"].sum().reset_index()
    fig = go.Figure(go.Pie(labels=df_pie["DESC_SECTOR"], values=df_pie["NUM_CONTRATOS"],
                           textinfo='label+percent',
                           insidetextorientation='radial'))

    fig.update_layout(
        font=dict(color='white'),
        template='plotly_dark'
    )

    return fig


colors = cl.scales['10']['qual']['Paired']
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("Analisis Descriptivo de la base de datos"), className="text-center mt-5 mb-5")
    ]),
    # Fila para los gráficos de barras
    dbc.Row([
        dbc.Col([
            html.H3("Contratos por Provincia y Género", className="text-center mt-5 mb-5"),
            dcc.Graph(id='bar-chart-genero', figure=create_bar_chart_genero(df_contratos_by_genero),
                      style={'height': '60vh', 'width': '100%'})
        ], width=4),
        dbc.Col([
            html.H3("Contratos por Provincia y Edad", className="text-center mt-5 mb-5"),
            dcc.Graph(id='bar-chart-edad', figure=create_bar_chart_edad(df_contratos_by_edad),
                      style={'height': '60vh', 'width': '100%'})
        ], width=4),
        dbc.Col([
            html.H3("Contratos por Provincia y Sector", className="text-center mt-5 mb-5"),
            dcc.Graph(id='bar-chart-sector', figure=create_bar_chart_sector(df_contratos_by_sector),
                      style={'height': '60vh', 'width': '100%'})
        ], width=4)
    ], className='mb-5'),

    # Fila para mostrar la tabla de grupos
    dbc.Row([
        dbc.Col([], width=2),  # Empty column at the left
        dbc.Col([
            html.H3("Tabla de los Grupos", className="text-center mt-5 mb-5"),
            dash_table.DataTable(
                id='table_grupos',
                columns=[{"name": i, "id": i} for i in df_grupos.columns],
                data=df_grupos.to_dict('records'),
                style_as_list_view=True,
                style_cell={
                    'padding': '10px',  # Increased padding
                    'backgroundColor': '#1e1e1e',  # Darker background color for cells
                    'color': '#f0f0f0',  # Lighter text color
                    'fontFamily': 'Arial',  # Easier to read font
                    'whiteSpace': 'normal',
                    'height': 'auto'
                },
                style_header={
                    'backgroundColor': '#15202b',
                    'fontWeight': 'bold',
                    'color': '#f0f0f0',  # Lighter text color
                    'fontFamily': 'Arial'  # Easier to read font
                },
                style_data_conditional=[
                    {
                        'if': {'row_index': 'odd'},  # Zebra stripes
                        'backgroundColor': '#212121'  # Slightly lighter for odd rows
                    },
                    {
                        'if': {'state': 'selected'},  # Highlight selected rows
                        'backgroundColor': '#565656',
                        'color': 'white'
                    }
                ],
                style_table={'overflowX': 'auto'},
            )
        ], width=8),  # Main column in the center
        dbc.Col([], width=2)  # Empty column at the right
    ], className='mb-5'),

    # Fila para mostrar los graficos de grupos
    dbc.Row([
        dbc.Col([
            html.H3("Contratos por Grupo", className="text-center mt-5 mb-5"),
            dcc.Graph(
                id='bar_contratos_by_grupo',
                figure={
                    'data': [
                        go.Bar(
                            x=[df_contratos_by_grupo['COD_GRUPO'][i]],
                            y=[df_contratos_by_grupo['total_contratos'][i]],
                            name=f'Grupo {df_contratos_by_grupo["COD_GRUPO"][i]}',
                            marker={'color': colors[i % len(colors)]}  # Use a color from the color scale
                        ) for i in range(df_contratos_by_grupo.shape[0])
                    ],
                    'layout': go.Layout(
                        template='plotly_dark'  # Dark theme
                    )
                }
            )
        ], width=4),  # Adjust the width here

        dbc.Col([
            html.H3("Contratos por Grupo y Edad", className="text-center mt-5 mb-5"),
            dcc.Graph(
                id='stacked_contratos_by_grupo_and_edad',
                figure={
                    'data': [
                        go.Bar(
                            x=df_contratos_by_grupo_and_edad[df_contratos_by_grupo_and_edad['RANGO_EDAD'] == edad][
                                'COD_GRUPO'],
                            y=df_contratos_by_grupo_and_edad[df_contratos_by_grupo_and_edad['RANGO_EDAD'] == edad][
                                'total_contratos'],
                            name=f'Edad {edad}'
                        ) for edad in df_contratos_by_grupo_and_edad['RANGO_EDAD'].unique()
                    ],
                    'layout': go.Layout(
                        barmode='stack',
                        template='plotly_dark'  # Dark theme
                    )
                }
            )
        ], width=4),  # Adjust the width here

        dbc.Col([
            html.H3("Contratos por Grupo y Género", className="text-center mt-5 mb-5"),
            dcc.Graph(
                id='grouped_contratos_by_grupo_and_genero',
                figure={
                    'data': [
                        go.Bar(
                            x=
                            df_contratos_by_grupo_and_genero[df_contratos_by_grupo_and_genero['DESC_GENERO'] == genero][
                                'COD_GRUPO'],
                            y=
                            df_contratos_by_grupo_and_genero[df_contratos_by_grupo_and_genero['DESC_GENERO'] == genero][
                                'total_contratos'],
                            name=f'{genero}'
                        ) for genero in df_contratos_by_grupo_and_genero['DESC_GENERO'].unique()
                    ],
                    'layout': go.Layout(
                        barmode='group',
                        template='plotly_dark'  # Dark theme
                    )
                }
            )
        ], width=4),  # Adjust the width here
    ], className='mb-5'),

    # Fila para el gráfico de barras y pastel
    dbc.Row([
        dbc.Col([
            html.H2("Contratos por mes", className="text-center mt-5 mb-5"),
            dcc.Graph(id='bar-chart', style={'height': '60vh', 'width': '100%'})
        ], width=6),
        dbc.Col([
            html.H2("Contratos por sector", className="text-center mt-5 mb-5"),
            dcc.Graph(id='pie-chart', style={'height': '60vh', 'width': '100%'})
        ], width=6)
    ], className='mb-5'),

    # Título de la página
    dbc.Row([
        dbc.Col(html.H1("Contratos por provincia"), className="text-center mt-5 mb-5")
    ]),

    # Fila para los checkboxes
    dbc.Row([
        dbc.Col([
            html.Label("Provincia"),
            dcc.Checklist(id='prov-checkbox',
                          options=[{'label': prov, 'value': prov} for prov in
                                   df_2019['NOM_PROV'].unique()],
                          value=['Alicante'],
                          inline=True)
        ], width=3),

        dbc.Col([
            html.Label("Sector"),
            dcc.Checklist(id='sector-checkbox',
                          options=[{'label': sector, 'value': sector} for sector in
                                   df_2019['DESC_SECTOR'].unique()],
                          value=['Agricultura y ganadería'],
                          inline=True)
        ], width=3),

        dbc.Col([
            html.Label("Género"),
            dcc.Checklist(id='genero-checkbox',
                          options=[{'label': genero, 'value': genero} for genero in
                                   df_2019['DESC_GENERO'].unique()],
                          value=['Hombres'],
                          inline=True)
        ], width=3),

        dbc.Col([
            html.Label("Rango de edad"),
            dcc.Dropdown(id='edad-dropdown',
                         options=[{'label': edad, 'value': edad} for edad in
                                  df_2019['RANGO_EDAD'].unique()],
                         clearable=False)
        ], width=3),
    ], className='mb-5'),

    # Fila para el mapa
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='mapa', style={'height': '80vh', 'width': '100%'})
        ])
    ], className='mb-5')
], fluid=True)


# Definir la función que actualiza el gráfico cuando cambian los filtros
@app.callback(
    Output('mapa', 'figure'),
    Input('prov-checkbox', 'value'),
    Input('sector-checkbox', 'value'),
    Input('genero-checkbox', 'value'),
    Input('edad-dropdown', 'value')
)
def update_choropleth(provincias, sectores, generos, edad):
    # Si no se selecciona ninguna opción, usar todos los valores posibles
    if not provincias:
        provincias = df_prov['NOM_PROV'].unique()
    if not sectores:
        sectores = df_prov['DESC_SECTOR'].unique()
    if not generos:
        generos = df_prov['DESC_GENERO'].unique()
    if not edad:
        edad = list(df_prov['RANGO_EDAD'].unique())

    filtered_df = df_prov[(df_prov['NOM_PROV'].isin(provincias)) &
                          (df_prov['DESC_SECTOR'].isin(sectores)) &
                          (df_prov['DESC_GENERO'].isin(generos)) &
                          (df_prov['RANGO_EDAD'].isin(edad))]

    if not filtered_df.empty:
        fig = px.choropleth(filtered_df, geojson=filtered_geojson, locations='COD_PROV',
                            color='NUM_CONTRATOS',
                            featureidkey='properties.cod_prov',
                            hover_name='NOM_PROV',
                            projection='mercator',
                            color_continuous_scale='plasma',
                            scope="europe",
                            template='plotly_dark')

        fig.update_geos(fitbounds="locations", visible=False)
        fig.update_layout(
            font=dict(color='white')
        )

        return fig
    else:
        fig = px.choropleth(df_prov, geojson=filtered_geojson, locations='COD_PROV',
                            color='NUM_CONTRATOS',
                            featureidkey='properties.cod_prov',
                            hover_name='NOM_PROV',
                            projection='mercator',
                            color_continuous_scale='plasma',
                            scope="europe",
                            template='plotly_dark')

        fig.update_geos(fitbounds="locations", visible=False)
        fig.update_layout(
            font=dict(color='white')
        )
        return fig


# Función de callback para actualizar el gráfico de barras al cargar la página
@app.callback(
    Output('bar-chart', 'figure'),
    Input('mapa', 'figure')  # Usa el mapa como una entrada "dummy" para activar la función al cargar la página
)
def update_bar_chart(dummy):
    return create_bar_chart_mes(df_2019)


# Función de callback para actualizar el gráfico de pastel al cargar la página
@app.callback(
    Output('pie-chart', 'figure'),
    Input('mapa', 'figure')  # Usa el mapa como una entrada "dummy" para activar la función al cargar la página
)
def update_pie_chart(dummy):
    return create_pie_chart()


if __name__ == '__main__':
    app.run_server(debug=True)
