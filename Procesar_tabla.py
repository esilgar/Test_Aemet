# procesar_tabla_bs4.py
import re

def grados_a_orientacion(grados):
    grados = float(grados)
    if 337.5 <= grados or grados < 22.5:
        return "Norte"
    elif 22.5 <= grados < 67.5:
        return "Noreste"
    elif 67.5 <= grados < 112.5:
        return "Este"
    elif 112.5 <= grados < 157.5:
        return "Sureste"
    elif 157.5 <= grados < 202.5:
        return "Sur"
    elif 202.5 <= grados < 247.5:
        return "Suroeste"
    elif 247.5 <= grados < 292.5:
        return "Oeste"
    elif 292.5 <= grados < 337.5:
        return "Noroeste"
    return "ND"

def procesar_filas_tabla(filas, nombre_ccaa, nombre_estacion):
    registro = {
        "Comunidad": nombre_ccaa,
        "Estación": nombre_estacion
    }

    for fila in filas[1:]:  # Saltamos cabecera
        columnas = fila.find_all("td")
        if len(columnas) != 2:
            continue

        variable = columnas[0].get_text(strip=True)
        valor_bruto = columnas[1].get_text(strip=True)

        if valor_bruto == "ND" and "viento" not in variable.lower():
            registro[f"{variable} valor"] = "ND"
            registro[f"{variable} mes"] = "ND"
            registro[f"{variable} año"] = "ND"
            continue

        if "viento" in variable.lower():
            match = re.search(r"Vel\s+(\d+),\s+Dir\s+(\d+)\s+\(\d{1,2}\s+(\w+)[.)]?\s+(\d{4})", valor_bruto)
            if match:
                vel, dir_grados, mes, anio = match.groups()
                orientacion = grados_a_orientacion(dir_grados)
                registro["Racha máx. viento: velocidad (km/h)"] = vel
                registro["Racha máx. viento: dirección"] = orientacion
                registro["Racha máx. viento: mes"] = mes
                registro["Racha máx. viento: año"] = anio
            else:
                registro["Racha máx. viento: velocidad (km/h)"] = "ND"
                registro["Racha máx. viento: dirección"] = "ND"
                registro["Racha máx. viento: mes"] = "ND"
                registro["Racha máx. viento: año"] = "ND"
            continue

        match = re.search(r"([\-\d.]+)\s*\((?:\d{1,2}\s+)?(\w+)[.)]?\s+(\d{4})", valor_bruto)
        if match:
            valor, mes, anio = match.groups()
        else:
            valor, mes, anio = valor_bruto, "ND", "ND"

        registro[f"{variable} valor"] = valor
        registro[f"{variable} mes"] = mes
        registro[f"{variable} año"] = anio

    return registro
