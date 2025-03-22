# AEMET Web Scraper

Este proyecto automatiza la recolección de datos climáticos extremos (efemérides) desde la web de AEMET utilizando Selenium y BeautifulSoup.

## 📦 Requisitos
⚠️ Este proyecto utiliza Selenium con el navegador Chrome, por lo que es necesario tener `chromedriver` en el mismo directorio donde se ejecuta el script `.py`. 
Puedes descargarlo desde: https://sites.google.com/chromium.org/driver/



Instala los paquetes necesarios con:

```
pip install -r requirements.txt
```

## 🚀 Uso

1. Ejecuta el script principal:

```bash
python aemet_Webscraping_Funciona_Todo.py
```

2. El script:
   - Accede a la web de AEMET.
   - Recorre todas las comunidades y estaciones.
   - Extrae datos de temperaturas, precipitaciones, vientos, etc.
   - Genera un CSV con toda la información: `efemerides_aemet_completo.csv`.

## 📁 Estructura del proyecto

- `aemet_Webscraping_Funciona_Todo.py`: Script principal con Selenium.
- `Procesar_tabla.py`: Función auxiliar para parsear HTML con BeautifulSoup.
- `requirements.txt`: Lista de librerías necesarias.
- `.env`: Variables de entorno (si usas alguna configuración personalizada).

## 🧑‍💻 Autor



