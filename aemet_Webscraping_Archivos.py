# Importamos las librerías necesarias
from selenium import webdriver
from selenium.webdriver.common.by import By
# By: Para buscar elementos por ID, nombre, clase, etc
from selenium.webdriver.support.ui import Select, WebDriverWait
# Select: maneja los desplegables  (<select>) en formularios HTML.
# WebDriverWait: Permite esperar a que algo ocurra en la página (como que cargue un elemento).
# Muy útil cuando hay contenido que tarda un poco en aparecer.
from selenium.webdriver.support import expected_conditions as EC
# expected_conditions as EC:  condiciones predefinidas que puedes usar con WebDriverWait, por ejemplo:

# - presence_of_element_located: espera a que el elemento exista en el DOM.
# - element_to_be_clickable: espera a que se pueda hacer clic en un botón.
# - visibility_of_element_located: espera a que un elemento sea visible.
from bs4 import BeautifulSoup #  Para leer y procesar el HTML (extraer tablas)
import pandas as pd
import time # Usamos sleep() para pausas breves si hace falta
import re # usaremos regular expressions para separar los campos de la tabla en formato dia/mes/año
import time as t
from Procesar_tabla import procesar_filas_tabla #función para hacer webscraping de la tabla con expresiones reguares

# INICIAMOS EL CONTADOR DE TIEMPO
start_time = t.time()

# Iniciamos el navegador con Selenium (Chrome en este caso)
driver = webdriver.Chrome()

# URL de la página de AEMET con las efemérides
url = "https://www.aemet.es/es/serviciosclimaticos/datosclimatologicos/efemerides_extremos"
driver.get(url)

# Esperamos a que el desplegable de comunidades autónomas cargue y guaramos los valores en select_ccaa

wait = WebDriverWait(driver, 10)

# Esperamos a que el selector de comunidades esté disponible: ccaa_selector
wait.until(EC.presence_of_element_located((By.ID, "ccaa_selector")))

# Seleccionamos el desplegable de comunidades
selector_comunidades = Select(driver.find_element(By.ID, "ccaa_selector"))
num_comunidades = len(selector_comunidades.options)  # numero de estaciones
# Lista para guardar todos los datos
datos = []

# Recorrer comunidades (saltamos el primer valor vacío)
for i in range(1, num_comunidades):
    comunidad = selector_comunidades.options[i]
    cod_ccaa = comunidad.get_attribute("value")
    nombre_ccaa = comunidad.text.strip()
    print(f"\n🟦 Comunidad: {nombre_ccaa}")

    selector_comunidades.select_by_value(cod_ccaa)

    # Localizamos el formulario
    formulario = driver.find_element(By.NAME, "frm1")
    # Buscamos el botón 'Buscar' dentro del formulario y lo pulsamos
    boton_buscar_comunidad = formulario.find_element(By.CSS_SELECTOR, "input[type='submit'].form_submit")
    boton_buscar_comunidad.click()


    # Esperamos a que cargue el selector de estaciones
    wait.until(EC.presence_of_element_located((By.ID, "estacion")))
    selector_estaciones = Select(driver.find_element(By.ID, "estacion"))
    num_estaciones = len(selector_estaciones.options) # numero de estaciones
    for j in range(1, num_estaciones):
        estacion = selector_estaciones.options[j]
        cod_estacion = estacion.get_attribute("value")
        nombre_estacion = estacion.text.strip()
        print(f"   📍 Estación: {nombre_estacion}")

        # Seleccionar estación
        selector_estaciones.select_by_value(cod_estacion)
        time.sleep(1)

        # Pulsar primer botón "Buscar" (formulario frm1)
        formulario = driver.find_element(By.NAME, "frm1")
        boton_buscar1 = formulario.find_element(By.CSS_SELECTOR, "input[type='submit'].form_submit")
        boton_buscar1.click()

        try:
            # Esperar selector de meses en la nueva página
            wait.until(EC.presence_of_element_located((By.ID, "meses")))

            # Seleccionar "Anual"
            selector_meses = Select(driver.find_element(By.ID, "meses"))
            selector_meses.deselect_all()
            selector_meses.select_by_value("13")

            # Seleccionar "todos" en variables
            selector_variables = Select(driver.find_element(By.ID, "variables"))
            selector_variables.deselect_all()
            selector_variables.select_by_value("todos")

            # Pulsar segundo botón "Buscar"
            # Localizamos el formulario por su ID
            formulario_final = driver.find_element(By.ID, "FrmCliEfemExtremos")

            # Dentro del formulario, localizamos el botón "Buscar"
            boton_buscar3 = formulario_final.find_element(By.CSS_SELECTOR, "input[type='submit'].form_submit")

            # Hacemos clic en el botón
            boton_buscar3.click()


            # Esperar tabla de resultados
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, "tabla_datos_sinpadd")))

            # Extraer tabla con BeautifulSoup
            soup = BeautifulSoup(driver.page_source, "html.parser")
            tabla = soup.find("table", class_="tabla_datos_sinpadd")
            filas = tabla.find_all("tr")

            # Pasamos los datos a la función que nos hará el webscaraping con RE
            registro = procesar_filas_tabla(filas, nombre_ccaa, nombre_estacion)
            datos.append(registro)

        except Exception as e:
            print(f"      ⚠️ Error en estación: {nombre_estacion}. {str(e)}")

        # Volver a la página de estaciones
        driver.get(url)
        wait.until(EC.presence_of_element_located((By.ID, "ccaa_selector")))
        selector_comunidades = Select(driver.find_element(By.ID, "ccaa_selector"))
        selector_comunidades.select_by_value(cod_ccaa)
        formulario = driver.find_element(By.NAME, "frm1")
        formulario.find_element(By.CSS_SELECTOR, "input[type='submit'].form_submit").click()
        wait.until(EC.presence_of_element_located((By.ID, "estacion")))
        selector_estaciones = Select(driver.find_element(By.ID, "estacion"))

    # Volver a la página de las ccaa
    driver.get(url)
    wait.until(EC.presence_of_element_located((By.ID, "ccaa_selector")))
    selector_comunidades = Select(driver.find_element(By.ID, "ccaa_selector"))
# Guardar en CSV
df = pd.DataFrame(datos)
df.to_csv("efemerides_aemet_completo.csv", index=False, encoding="utf-8-sig")
print("\n✅ Proceso finalizado. Archivo guardado como 'efemerides_aemet_completo.csv'.")

# TIEMPO FINAL
end_time = t.time()
duration = end_time - start_time
print(f"⏱️ Tiempo total de ejecución: {duration:.2f} segundos")

driver.quit()