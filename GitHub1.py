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
    # ASI NO FUNCIONA UN CICLO EN PYTHON !!!, tienes que usar range
    for pagina in range(cant_paginas):
        print(pagina)
        # CON PAGE_SOURCE OBTENGO EL CONTENIDO HTML DE LA PAGINA ACTUAL
        contenido_pagina = navegador.page_source  # <--- AGREGUE ESTO
        # pagina = requests.get(url=paginaN) NO LO OCUPAS
        soup = BeautifulSoup(contenido_pagina, "html.parser")
        # CAMBIE LA CLASE, PORQUE LA OTRA CHOCABA CON OTROS ELEMENTOS QUE NO ERAN PRODUCTOS.
        productos = soup.find_all('div', attrs={'class': 'a-section a-spacing-base'})
        # botonSiguiente = soup.find('a', attrs={'class': 's-pagination-item s-pagination-next s-pagination-button s-pagination-separator'})
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
    navegador.close()

def amazonUS(busqueda):
    # testeo para probar barras de busqueda
    global datos
    # mandar comando a la barra de busqueda para que escriba el item escrito y hacer el web scrapping desde la pagina que resulte
    navegador = webdriver.Chrome(service=s, options=opc)
    navegador.get("https://www.amazon.com/")
    barra = navegador.find_element(By.ID, value="twotabsearchtextbox")
    time.sleep(2)
    barra.send_keys(busqueda)
    time.sleep(3)
    barra.send_keys(Keys.ENTER)
    time.sleep(10)
    navegador.close()


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
    navegador.close()


bestBuy("s22")

data_df = pd.DataFrame(datos)
print(data_df)