import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import mysql.connector
import numpy as np

def conectar():
    conexion = mysql.connector.connect(
        host='localhost',
        port='3306',
        user='root',
        password='',
        database='proyecto')
    print("Conexion exitosa")
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM tienda")
    consulta = cursor.fetchall()
    for i in consulta:
        print(i)


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

dashboard1 = 0
dashboard2 = 0
dashboard3 = 0
def creardf():
    dataframe = pd.DataFrame(datos)
    dataframe = dataframe[dataframe["Precio"] != "No disponible"]
    dataframe = dataframe[dataframe["Calificacion"] != "No disponible"]
    dataframe = dataframe[dataframe["Puntuaciones"] != 0]
    dataframe["Calificacion"] = dataframe["Calificacion"].apply(lambda x: x[:3])
    print(dataframe)
    dataframe.to_csv("C:/Users/ecuri/Desktop/dataset.csv")

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
    opcion = int(input("\nOpciones\n1. Sobre el programa\n2. Extraer datos\n3. Crear dataframe \n4. Opciones de la base de datos. \n5. Obtener Dashboards.\n6. Salir.\n "))
    if opcion == 1:
        print("Texto texto texto")
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
    elif opcion == 4:
        acc = int(input("Opciones \n1. Acceder a la base de datos. \n2. Subir datos a la base de datos\n"))
        if acc == 1:
            conectar()
        elif acc == 2:
            pass
        else:
            print("Comando invalido")
    elif opcion == 5:
        print("aun nada")
        pass
    elif opcion == 6:
        print("Adios")
        break
    else:
        print("Comando invalido")