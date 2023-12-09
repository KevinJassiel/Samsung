import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import pymongo
from pymongo import MongoClient
import plotly.express as px
import dash
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html

def subir():
    myclient = pymongo.MongoClient("mongodb://localhost:27017")
    mydb = myclient["mercado_gris"]
    mycol = mydb["productos_encontrados"]
    registros = dataframe.to_dict(orient='records')
    mycol.insert_many(registros)
    print("Hecho con exito")


def dashboards():
    myclient = pymongo.MongoClient("mongodb://localhost:27017")
    mydb = myclient["mercado_gris"]
    mycol = mydb["productos_encontrados"]

    documentos = mycol.find()

    campos_a_convertir = ["Calificacion", "Puntuaciones"]
    for documento in documentos:
        for campo in campos_a_convertir:
            valor_cadena = documento.get(campo)
            if valor_cadena:
                try:
                    valor_numerico = float(valor_cadena)
                    # Actualizar el campo en el documento con el valor numérico
                    mycol.update_one({"_id": documento["_id"]}, {"$set": {campo: valor_numerico}})
                except ValueError:
                    print(f"No se pudo convertir a número: {valor_cadena} en el campo {campo}")
    pipeline = [
        {"$group": {"_id": "$Pais", "promedio_calificacion": {"$avg": "$Calificacion"}}},
        {"$match": {"promedio_calificacion": {"$lte": 5}}}
    ]

    resultados = list(mycol.aggregate(pipeline))
    df = pd.DataFrame(resultados)
    # Graficar con Plotly
    fig = px.bar(df, x='_id', y='promedio_calificacion',
                 labels={'_id': 'País', 'promedio_calificacion': 'Promedio de Calificación'})
    fig.update_layout(title='Promedio de Calificación por País', xaxis_title='País',
                      yaxis_title='Promedio de Calificación')
    fig.show()

    #grafica con dash
    pipeline2 = [
        {"$group": {"_id": "$Pais", "promedio_calificacion": {"$avg": "$Calificacion"},
                    "suma_puntuaciones": {"$sum": "$Puntuaciones"}}}
    ]

    resultados2 = list(mycol.aggregate(pipeline2))

    # Crear un DataFrame con los resultados
    df2 = pd.DataFrame(resultados2)
    # Gráfico de barras para el promedio de Calificacion por Pais
    fig_promedio_calificacion = px.bar(df2, x='_id', y='promedio_calificacion',
                                       labels={'_id': 'País', 'promedio_calificacion': 'Promedio de Calificación'})
    fig_promedio_calificacion.update_layout(title='Promedio de Calificación por País', xaxis_title='País',
                                            yaxis_title='Promedio de Calificación')
    # Gráfico de barras para la suma de Puntuaciones por Pais
    fig_suma_puntuaciones = px.bar(df2, x='_id', y='suma_puntuaciones',
                                   labels={'_id': 'País', 'suma_puntuaciones': 'Suma de Puntuaciones'})
    fig_suma_puntuaciones.update_layout(title='Suma de Puntuaciones por País', xaxis_title='País',
                                        yaxis_title='Suma de Puntuaciones')
    # Inicializar la aplicación Dash
    app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
    # Diseño del dashboard
    app.layout = dbc.Container([
        html.H1("Dashboard - País, Promedio de Calificación y Suma de Puntuaciones"),
        dbc.Row([
            dbc.Col(dcc.Graph(figure=fig_promedio_calificacion), width=6),
            dbc.Col(dcc.Graph(figure=fig_suma_puntuaciones), width=6)
        ]),
        dbc.Table.from_dataframe(df2, striped=True, bordered=True, hover=True)
    ])
    if __name__ == '__main__':
        app.run_server(debug=True)


def dashboard2():
    myclient = pymongo.MongoClient("mongodb://localhost:27017")
    mydb = myclient["mercado_gris"]
    mycol = mydb["productos_encontrados"]

    paises = mycol.distinct("Pais")
    # Consultar los primeros 10 documentos que cumplan con las condiciones por país
    resultados = []
    for pais in paises:
        consulta = {"Pais": pais, "Calificacion": {"$gt": 3.5}, "Puntuaciones": {"$gt": 20}}
        documentos = list(mycol.find(consulta, {"Calificacion": 1, "Puntuaciones": 1}).limit(10))
        resultados.extend(documentos)
    df = pd.DataFrame(resultados)
    # Gráfico de dispersión con Plotly
    fig = px.scatter(df, x='Calificacion', y='Puntuaciones', color='Pais',
                     labels={'Calificacion': 'Calificación', 'Puntuaciones': 'Puntuaciones'})
    fig.update_layout(title='Calificación vs Puntuaciones por País (Relacion de cantidad de puntuaciones con Calificacion)',
                      xaxis_title='Calificación', yaxis_title='Puntuaciones')
    fig.show()


s = Service(ChromeDriverManager().install())
opc = Options()
opc.add_argument("--window-size= 1020, 1200")

datos = {
    "Marca": [],
    "Tienda": [],
    "Pais": [],
    "Producto": [],
    "Precio": [],
    "Calificacion": [],
    "Puntuaciones": []
}

dataframe = 0


def creardf():
    global dataframe
    dataframe = pd.DataFrame(datos)
    dataframe = dataframe[dataframe["Precio"] != "No disponible"]
    dataframe = dataframe[dataframe["Calificacion"] != "No disponible"]
    dataframe = dataframe[dataframe["Puntuaciones"] != 0]
    dataframe["Calificacion"] = dataframe["Calificacion"].apply(lambda x: x[:3])
    return dataframe

def amazonMx(busqueda, pgs):
    global datos
    # mandar comando a la barra de busqueda para que escriba el item escrito y hacer el web scrapping desde la pagina que resulte
    navegador = webdriver.Chrome(service=s, options=opc)
    navegador.get("https://www.amazon.com.mx/")
    barra = navegador.find_element(By.ID, value="twotabsearchtextbox")
    time.sleep(2)
    barra.send_keys(busqueda)
    time.sleep(3)
    barra.send_keys(Keys.ENTER)

    for pagina in range(pgs - 1):
        print(pagina)
        contenido_pagina = navegador.page_source
        soup = BeautifulSoup(contenido_pagina, "html.parser")
        productos = soup.find_all('div', attrs={'class': 'a-section a-spacing-base'})
        botonSiguiente = navegador.find_element(By.LINK_TEXT, "Siguiente")
        # i va a equivaler a cada producto disponible en la pagina porque comparten el atributo del soup
        for i in productos:
            marca = "Samsung"
            tienda = "Amazon"
            pais = "Mexico"
            producto = i.find("span", attrs={"class": "a-size-base-plus a-color-base a-text-normal"}).text
            # AGREGUE LOS .TEXT ANTES, PORQUE SI LOS AGREGAS ABAJO MARCA ERROR.
            try:
                precio = i.find("span", attrs={"class": "a-price-whole"}).text
            except:
                precio = "No disponible"
            # AGREGUE EL TRY A VECES HAY PRODUCTOS SIN CALIFICAR.
            try:
                calificacion = i.find('span', attrs={"class": "a-icon-alt"}).text
            except:
                calificacion = "No disponible"
            try:
                puntuaciones = i.find('span', attrs={"class": "a-size-base s-underline-text"}).text
            except:
                puntuaciones = 0
            datos["Marca"].append(marca)
            datos["Tienda"].append(tienda)
            datos["Pais"].append(pais)
            datos["Producto"].append(producto)
            datos["Precio"].append(precio)
            datos["Calificacion"].append(calificacion)
            datos["Puntuaciones"].append(puntuaciones)
        try:
            botonSiguiente.click()
        except:
            print("No se pudo acceder a la siguiente pagina o no existe una siguiente pagina")
            break
        time.sleep(5)
    navegador.close()

def amazonUS(busqueda, pgs):
    global datos
    # mandar comando a la barra de busqueda para que escriba el item escrito y hacer el web scrapping desde la pagina que resulte
    navegador = webdriver.Chrome(service=s, options=opc)
    navegador.get("https://www.amazon.com/")
    time.sleep(10)
    barra = navegador.find_element(By.ID, value="twotabsearchtextbox")
    time.sleep(2)
    barra.send_keys(busqueda)
    time.sleep(3)
    barra.send_keys(Keys.ENTER)
    time.sleep(10)

    for pagina in range(pgs - 1):
        print(pagina)
        contenido_pagina = navegador.page_source
        soup = BeautifulSoup(contenido_pagina, "html.parser")
        productos = soup.find_all("div", attrs={"class":"a-section a-spacing-small a-spacing-top-small"})
        botonSiguiente = navegador.find_element(By.LINK_TEXT, "Next")
        # i va a equivaler a cada producto disponible en la pagina porque comparten el atributo del soup
        for i in productos[1:]:
            marca = "Samsung"
            tienda = "Amazon"
            pais = "USA"
            producto = i.find("span", attrs={"class": "a-size-medium a-color-base a-text-normal"}).text
            try:
                precio = i.find("span", attrs={"class": "a-price-whole"}).text
            except:
                precio = "No disponible"
            try:
                calificacion = i.find('span', attrs={"class": "a-icon-alt"}).text
            except:
                calificacion = "No disponible"
            try:
                puntuaciones = i.find('span', attrs={"class": "a-size-base s-underline-text"}).text
            except:
                puntuaciones = 0
            datos["Marca"].append(marca)
            datos["Tienda"].append(tienda)
            datos["Pais"].append(pais)
            datos["Producto"].append(producto)
            datos["Precio"].append(precio)
            datos["Calificacion"].append(calificacion)
            datos["Puntuaciones"].append(puntuaciones)
        try:
            botonSiguiente.click()
        except:
            print("No se pudo acceder a la siguiente pagina o no existe una siguiente pagina")
            break
        time.sleep(5)
    navegador.close()


while True:
    print("-------Menu Proyecto final Programacion para la extraccion de datos-------")
    opcion = int(input("\nOpciones\n1. Sobre el programa\n2. Extraer datos\n3. Crear dataframe \n4. Subir a la base de datos. \n5. Obtener Dashboards.\n6. Salir.\n "))
    if opcion == 1:
        print("Lorem imsum")
        input(" ")
    elif opcion == 2:
        print("Webs de donde es posible extraer datos:")
        web = int(input("\n1. Amazon Mexico. \n2. Amazon de Estados Unidos.\n "))
        if web == 1:
            pags = int(input("De cuantas paginas quieres extraer los datos (cantidad) "))
            prd = input("Cual es el producto samsung que deseas buscar? solo es necesario el modelo ")
            amazonMx(prd, pags)
            input(" ")
        elif web == 2:
            pags = int(input("De cuantas paginas quieres extraer los datos (cantidad) "))
            prd = input("Cual es el producto samsung que deseas buscar? solo es necesario el modelo ")
            amazonUS(prd, pags)
            input(" ")
        else:
            print("Comando invalido")
    elif opcion == 3:
        creardf()
        print(dataframe)
    elif opcion == 4:
        if len(dataframe) == 0:
            print("Datos insuficientes")
        else:
            subir()
    elif opcion == 5:
        dashboards()
        dashboard2()
    elif opcion == 6:
        print("Adios")
        break
    else:
        print("Comando invalido")