import pandas as pd
import json
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn import metrics
# Cargar los datos que se quieren graficar
df_2019 = pd.read_csv("../DB/2019/contratos_por_municipio-sector-grupo_ocupacion-genero-edad-2019.csv", sep=";")

"""
# Convertir la columna de rango de edad en valores numéricos
def convert_age_range_to_numeric(age_range):
    age_range = age_range.strip() # Elimina espacios al principio y al final
    if age_range == '<25':
        return 24
    elif age_range == '>44':
        return 45
    else:
        lower, upper = age_range.split("-")
        return (float(lower) + float(upper)) / 2

df_regression = df_2019

print(df_2019["RANGO_EDAD"].unique())

df_regression["RANGO_EDAD"] = df_regression["RANGO_EDAD"].apply(convert_age_range_to_numeric)

# Asegúrate de que las columnas sean numéricas
df_regression["RANGO_EDAD"] = pd.to_numeric(df_regression["RANGO_EDAD"], errors='coerce')
df_regression["NUM_CONTRATOS"] = pd.to_numeric(df_regression["NUM_CONTRATOS"], errors='coerce')

# Remueve los valores NA después de la conversión
df_regression = df_regression.dropna()

# Definir las variables X y y
X = df_regression['RANGO_EDAD'].values.reshape(-1,1)
y = df_regression['NUM_CONTRATOS'].values.reshape(-1,1)

# Dividir los datos en conjuntos de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

# Entrenar el algoritmo
regressor = LinearRegression()
regressor.fit(X_train, y_train)

# Hacer predicciones
y_pred = regressor.predict(X_test)

# Comparar los resultados
df = pd.DataFrame({'Edad Real': X_test.flatten(), 'Contratos Predichos': y_pred.flatten()})
print(df)"""
df_2019['RANGO_EDAD'] = df_2019['RANGO_EDAD'].str.strip()
one_hot = pd.get_dummies(df_2019, columns=['RANGO_EDAD'])


# Preparar los datos
X = one_hot[['RANGO_EDAD_<25', 'RANGO_EDAD_25-44', 'RANGO_EDAD_>44']]
print(X)
y = one_hot['NUM_CONTRATOS']

# Crear el modelo
model = LinearRegression()

# Ajustar el modelo
model.fit(X, y)

# Imprimir los coeficientes
print("Intercepto: ", model.intercept_)
print("Coeficientes: ", model.coef_)

# Ahora puede usar este modelo para hacer predicciones
one_hot['Contratos Predichos'] = model.predict(X)