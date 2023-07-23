import traceback

from flask import Flask, render_template, request

# Forms
from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField

# Graphs
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio

# DB
from sqlalchemy import create_engine
from sqlalchemy import text
import json

server = Flask(__name__)

# Configuración de la conexión a la base de datos MySQL
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'dbtfm',
}


class FilterForm(FlaskForm):
    servicios = SelectField('Servicios', choices=[])
    provincia = SelectField('Provincia', choices=[])
    edad = SelectField('Edad', choices=[])
    genero = SelectField('Género', choices=[])
    submit = SubmitField('Actualizar gráfico')


# Funciones para generar los graficos

# Número de contratos por fecha
def generate_graph_contratos_by_fecha():
    # Crear la cadena URI para la conexión de SQLAlchemy
    db_uri = f"mysql+pymysql://{db_config['user']}:{db_config['password']}@{db_config['host']}/{db_config['database']}"

    try:
        # Crear el engine de SQLAlchemy y la conexión
        engine = create_engine(db_uri)
        connection = engine.connect()

        # Consulta SQL para obtener los datos de la tabla
        query = text("SELECT FECHA, SUM(NUM_CONTRATOS) AS NUM_CONTRATOS FROM contratos GROUP BY FECHA;")

        # Obtener los datos del DataFrame pandas
        df_contratos = pd.read_sql_query(query, connection)

        # Cerrar la conexión a la base de datos
        connection.close()

        # Crear figura usando objetos gráficos de plotly
        fig = go.Figure()

        # Agregar traza de línea
        fig.add_trace(
            go.Scatter(x=df_contratos['FECHA'], y=df_contratos['NUM_CONTRATOS'], mode='lines', name='NUM_CONTRATOS',
                       line=dict(color='blue'))
        )

        # Establecer las propiedades del layout
        fig.update_layout(
            title='Número de contratos por fecha',
            title_x=0.5,
            xaxis=dict(
                title='Fecha',
                showgrid=True,  # agrega la cuadrícula
                gridcolor='LightPink',  # puedes cambiar el color de la cuadrícula si quieres
            ),
            yaxis=dict(
                title='Número de contratos',
                showgrid=True,
                gridcolor='LightPink',
            ),
            font=dict(
                family='Courier New, monospace',  # puedes cambiar la fuente si quieres
                size=12,
                color='RebeccaPurple'  # puedes cambiar el color del texto si quieres
            ),
            plot_bgcolor='white'  # cambia el color de fondo si quieres
        )

        return pio.to_html(fig, full_html=False)

    except Exception as e:
        print("Error en la conexión o en la consulta SQL:", e)
        print(traceback.format_exc())


# Mapa Interactivo
def generate_graph_mapa():
    df_temp = pd.read_csv("../DB/db_mapa.csv", encoding='utf-8', dtype={'id': str})

    with open('../DB/municipios.geojson', encoding='utf-8') as json_file:
        municipios = json.load(json_file)

    # Crea el mapa coroplético
    fig = px.choropleth(df_temp, geojson=municipios, locations='id', color='COLOR',
                        color_continuous_scale="plasma",
                        scope="europe",
                        hover_name='NOM_MUN',
                        hover_data={'NUM_CONTRATOS': True, 'COLOR': False, 'id': False},
                        fitbounds='locations',
                        projection='mercator'
                        )

    # Crea un gráfico de dispersión geográfico con el tamaño de los puntos proporcional al número de contratos
    fig2 = px.scatter_geo(df_temp, lat='lat', lon='lon', size='NUM_CONTRATOS',
                          hover_data={'NUM_CONTRATOS_FORMATTED': False, 'NOM_MUN': False, 'lat': False, 'lon': False},
                          custom_data=['NOM_MUN', 'NUM_CONTRATOS_FORMATTED'],
                          projection='mercator')

    fig2.update_traces(hovertemplate='<b>%{customdata[0]}</b><br>Contratos: %{customdata[1]}<extra></extra>')

    # Combina los dos gráficos
    fig.add_trace(fig2.data[0])

    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    fig.update_layout(coloraxis_colorbar=dict(title='Contratos', tickprefix='1.e'))

    return pio.to_html(fig, full_html=False)


@server.route('/')
def index():
    return render_template('index.html')


@server.route('/home')
def home():
    return render_template('home.html')


@server.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


@server.route('/analisis')
def analisis():
    # Genera el gráfico y conviértelo en HTML
    df = px.data.iris()
    fig = px.scatter(df, x="sepal_width", y="sepal_length")
    fig_html = pio.to_html(fig, full_html=False)

    return render_template('analisis.html', plot=fig_html)


@server.route('/grafico', methods=['GET', 'POST'])
def grafico():
    # Genera el gráfico y conviértelo en HTML
    df = px.data.iris()
    fig = px.scatter(df, x="sepal_width", y="sepal_length")

    # Pasa el HTML a la plantilla
    return render_template('grafico.html', plot=generate_graph_mapa())


if __name__ == '__main__':
    server.debug = True
    server.run(debug=True)
