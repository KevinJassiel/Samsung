import requests
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

def conectar():
    try:
        conexion = mysql.connector.connect(host=´localhost´,
                                           port=´3306´,
                                           user=´root´,
                                           password=´user´,
                                           db=´proyecto´)
if conexion.is_connected():
    print("Se ha logrado la conexion")
    informacion = conexion.get_server_info()
    print(informacion)
    cursor = conexion.cursor()
    cursor.execute("SLECT DATABASE()")
    #Usamos fetchone porque solamente seleccionaremos una bade de datos, proyecto
    row=cursor.fetchone()
    print("conectado a:{}".format(row))
except Exception as error;
    print("No se logro completar la conexion")

#seleccionamos 
cursor.execute("SELECT * FROM tienda")

#obtenemos todos los resultados
tiendas=cursor.fetchall()
for i in tiendas:
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


def amazonMx(busqueda):
    global datos
    # mandar comando a la barra de busqueda para que escriba el item escrito y hacer el web scrapping desde la pagina que resulte
    navegador = webdriver.Chrome(service=s, options=opc)
    navegador.get("https://www.amazon.com.mx/")
    barra = navegador.find_element(By.ID, value="twotabsearchtextbox")
    time.sleep(2)
    barra.send_keys(busqueda)
    time.sleep(3)
    barra.send_keys(Keys.ENTER)

    cant_paginas = 2
    for pagina in range(cant_paginas):
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
            # PORQUE EJEMPLO SI NO HAY PRECIO PONES NO DISPONIBLE DIRECTO ESO ES
            # UNA CADENA POR LO QUE NO TIENE EL ATRIBUTO TEXT.
            # SI EXISTIERA ENTRA EL TRY, EL FIND REGRESA UN OBJETO QUE TIENE EL ATRIBUTO TEXT
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
    navegador.close()  # <-- LO SAQUE DEL CICLO, PORQUE CIERRA EL NAVEGADOR, ANTES DE ACABAR EL CICLO DE LAS PAGINAS

def mercadoLibre(busqueda):
    #testeo para probar barras de busqueda
    global datos
    # mandar comando a la barra de busqueda para que escriba el item escrito y hacer el web scrapping desde la pagina que resulte
    navegador = webdriver.Chrome(service=s, options=opc)
    navegador.get("https://www.mercadolibre.com.mx/")
    barra = navegador.find_element(By.ID, value="cb1-edit")
    time.sleep(2)
    barra.send_keys(busqueda)
    time.sleep(3)
    barra.send_keys(Keys.ENTER)
    time.sleep(10)

    cant_paginas = 3
    for pagina in range(cant_paginas):
        print(pagina)
        # con page_source se obtiene el contenido HTML de la pagina actual
        contenido_pagina = navegador.page_source
        soup = BeautifulSoup(contenido_pagina, "html.parser")
        productos = soup.find_all('div', attrs={'class': 'andes-card ui-search-result ui-search-result--core andes-card--flat andes-card--padding-16'})
        botonSiguiente = navegador.find_element(By.CLASS_NAME, "andes-pagination__arrow-title")
        # i va a equivaler a cada producto disponible en la pagina porque comparten el atributo del soup
        for i in productos:
            marca = "Samsung"
            tienda = "Mercado Libre"
            pais = "Mexico"
            producto = i.find("h2", attrs={"class": "ui-search-item__title"}).text
            # AGREGUE LOS .TEXT ANTES, PORQUE SI LOS AGREGAS ABAJO MARCA ERROR.
            # PORQUE EJEMPLO SI NO HAY PRECIO PONES NO DISPONIBLE DIRECTO ESO ES
            # UNA CADENA POR LO QUE NO TIENE EL ATRIBUTO TEXT.
            # SI EXISTIERA ENTRA EL TRY, EL FIND REGRESA UN OBJETO QUE TIENE EL ATRIBUTO TEXT
            try:
                precio = i.find("span", attrs={"class": "andes-money-amount__fraction"}).text
            except:
                precio = "No disponible"
            try:
                calificacion = i.find('span', attrs={"class": "ui-search-reviews__rating-number"}).text
            except:
                calificacion = "No disponible"
            try:
                puntuaciones = i.find('span', attrs={"class": "ui-search-reviews__amount"}).text
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
    navegador.close()  # <-- LO SAQUE DEL CICLO, PORQUE CIERRA EL NAVEGADOR, ANTES DE ACABAR EL CICLO DE LAS PAGINAS

def amazonUS(busqueda):
    # testeo para probar barras de busqueda
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

    cant_paginas = 2
    for pagina in range(cant_paginas):
        print(pagina)
        contenido_pagina = navegador.page_source
        soup = BeautifulSoup(contenido_pagina, "html.parser")
        productos = soup.find_all('div', attrs={'class': 'puisg-row'})
        botonSiguiente = navegador.find_element(By.LINK_TEXT, "Next")
        # i va a equivaler a cada producto disponible en la pagina porque comparten el atributo del soup
        for i in productos:
            marca = "Samsung"
            tienda = "Amazon"
            pais = "USA"
            #Si no pongo punto text me regresatodo el valor de la etiqueta, si si pongo .text
            #  me marca error 'NoneType' object has no attribute 'text'
            product = i.find("span", attrs={"class": "a-size-medium a-color-base a-text-normal"})
            sopa = BeautifulSoup(product, 'html.parser')
            producto = sopa.get_text()
            #.TEXT PORQUE SI LOS AGREGAS ABAJO MARCA ERROR.
            # SI EXISTIERA ENTRA EL TRY, EL FIND REGRESA UN OBJETO QUE TIENE EL ATRIBUTO TEXT
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
    navegador.close()  # <-- LO SAQUE DEL CICLO, PORQUE CIERRA EL NAVEGADOR, ANTES DE ACABAR EL CICLO DE LAS PAGINAS


def bestBuy(busqueda):
    # testeo para probar barras de busqueda
    global datos
    # mandar comando a la barra de busqueda para que escriba el item escrito y hacer el web scrapping desde la pagina que resulte
    navegador = webdriver.Chrome(service=s, options=opc)
    navegador.get("https://www.bestbuy.com/")
    time.sleep(3)
    #Esto se hace porque bestbuy te pide seleccionar un pais para comprar (en este caso usamos us) entonces debemos buscar el id del boton de US y presionarlo
    us = navegador.find_element(By.CLASS_NAME, value="us-link")
    us.click()
    time.sleep(4)
    barra = navegador.find_element(By.ID, value="gh-search-input")
    time.sleep(2)
    barra.send_keys(busqueda)
    time.sleep(3)
    barra.send_keys(Keys.ENTER)
    time.sleep(10)

    cant_paginas = 2
    for pagina in range(cant_paginas):
        print(pagina)
        contenido_pagina = navegador.page_source
        soup = BeautifulSoup(contenido_pagina, "html.parser")
        productos = soup.find_all('div', attrs={'class': 'shop-sku-list-item'})
        botonSiguiente = navegador.find_element(By.CLASS_NAME, "sku-list-page-next")
        # i va a equivaler a cada producto disponible en la pagina porque comparten el atributo del soup
        for i in productos:
            marca = "Samsung"
            tienda = "Best Buy"
            pais = "USA"
            producto = i.find("h4", attrs={"class": "sku-title"}).text
            # .TEXT PORQUE SI LOS AGREGAS ABAJO MARCA ERROR.
            # SI EXISTIERA ENTRA EL TRY, EL FIND REGRESA UN OBJETO QUE TIENE EL ATRIBUTO TEXT
            try:
                precio = i.find("div", attrs={"class": "priceView-hero-price priceView-customer-price"}).text
            except:
                precio = "No disponible"
            try:
                calificacion = i.find('p', attrs={"class": "visually-hidden"}).text
            except:
                calificacion = "No disponible"
            try:
                puntuaciones = i.find('span', attrs={"class": "c-reviews "}).text
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
    navegador.close()  # <-- LO SAQUE DEL CICLO, PORQUE CIERRA EL NAVEGADOR, ANTES DE ACABAR EL CICLO DE LAS PAGINAS


amazonUS("s22")

data_df = pd.DataFrame(datos)
print(data_df)
data_df.to_csv("C:/Users/ecuri/Desktop/dataset.csv")
