import pandas as pd
import plotly.express as px
import json
import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# cargar los datos que se quieren graficar
df19 = pd.read_csv("../DB/2019/contratos_por_municipio-sector-grupo_ocupacion-genero-edad-2019.csv", sep=";")
df19 = df19.drop(columns=['ANYO', 'COD_MUN', 'NOM_MUN', 'COD_SECTOR', 'COD_GRUPO', 'DESC_GRUPO', 'DESC_GENERO'])

pd.set_option('display.max_columns', None)
print(len(df19))
print(df19.dtypes)

df19 = df19.groupby(['MES', 'COD_GENERO', 'COD_PROV', 'NOM_PROV'])['NUM_CONTRATOS'].sum().to_frame()
df19.reset_index(inplace=True)
df19['COD_PROV'] = df19['COD_PROV'].astype(str)
df19.loc[df19['COD_PROV'] == '3', 'COD_PROV'] = '03'
print(df19[:5])

# Agregar la estadística descriptiva
stats_df = df19.describe()
# Esto hará que las estadísticas (mean, count, std, etc.) se muestren como una columna en lugar de como índices de fila
stats_df.reset_index(inplace=True)


# Para poder graficar en el mapa necesitamos las localizaciones.
with open('../DB/spain-provinces.geojson', 'r', encoding='utf-8') as f:
    geojson = json.load(f)

# filtrar el geojson para mostrar solo las provincias de Alicante, Castellón y Valencia
provincias = ['03', '12', '46']  # códigos de las provincias de Alicante, Castellón y Valencia
filtered_geojson = {
    'type': 'FeatureCollection',
    'features': [feature for feature in geojson['features']
                 if feature['properties']['cod_prov'] in provincias]
}

print(filtered_geojson)

# crear el gráfico choropleth con el geojson y los datos filtrados
fig = px.choropleth_mapbox(df19, geojson=filtered_geojson, locations='COD_PROV',
                           color='NUM_CONTRATOS',
                           featureidkey='properties.cod_prov',
                           hover_name='NOM_PROV',  # Agregar el nombre de la provincia como etiqueta al hacer hover
                           center={"lat": 40.4168, "lon": -3.7038},
                           mapbox_style="carto-positron", zoom=5)

fig.update_layout(title_text='Contratos por provincia')

fig.show()

fig2 = px.choropleth(df19, geojson=filtered_geojson, locations='COD_PROV',
                     color='NUM_CONTRATOS',
                     featureidkey='properties.cod_prov',
                     hover_name='NOM_PROV',  # Agregar el nombre de la provincia como etiqueta al hacer hover
                     projection='mercator',
                     title='Contratos por provincia',
                     color_continuous_scale='plasma')

fig2.update_geos(fitbounds="locations", visible=False)

fig2.show()

#
#
# df19 = pd.read_csv("DB/2019/contratos_por_municipio-sector-grupo_ocupacion-genero-edad-2019.csv", sep=";")
# df19 = df19.drop(columns=['ANYO', 'COD_MUN', 'NOM_MUN', 'COD_SECTOR', 'COD_GRUPO', 'DESC_GRUPO', 'DESC_GENERO'])
#
# pd.set_option('display.max_columns', None)
# print(len(df19))
# print(df19.dtypes)
#
# df19 = df19.groupby(['MES', 'COD_GENERO', 'NOM_PROV'])['NUM_CONTRATOS'].mean()
#
# print(df19.head(24).to_string())
# print(len(df19))
#
# geoJson = pd.read_csv('https://raw.githubusercontent.com/codeforgermany/click_that_hood/main/public/data/spain'
#                       '-provinces.geojson')
#
# prueba = pd.DataFrame({
#     'provincia': ['Alicante', 'Castellón', 'Valencia'],
#     'poblacion': [1950000, 580000, 2580000]
# })
#
# mapping = {
#     'Alicante / Alacant': 'Alicante',
#     'Castelló / Castellón': 'Castellón',
#     'València / Valencia': 'Valencia'
# }
#
# fig = px.choropleth(
#     prueba,
#     locations=prueba['provincia'],
#     locationmode='geojson-id',
#     geojson=geojson,
#     color='poblacion',
#     color_continuous_scale='YlOrRd',
#     featureidkey='properties.name',
#     labels={'poblacion': 'Población'}
# )
# fig.show()
