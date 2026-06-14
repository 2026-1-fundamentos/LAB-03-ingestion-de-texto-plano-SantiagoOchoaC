"""
Escriba el codigo que ejecute la accion solicitada en cada pregunta.
"""

# pylint: disable=import-outside-toplevel

def pregunta_01():
    """
    Construya y retorne un dataframe de Pandas a partir del archivo
    'files/input/clusters_report.txt'. Los requierimientos son los siguientes:

    - El dataframe tiene la misma estructura que el archivo original.
    - Los nombres de las columnas deben ser en minusculas, reemplazando los
      espacios por guiones bajos.
    - Las palabras clave deben estar separadas por coma y con un solo
      espacio entre palabra y palabra.


    """
    import re
    import pandas as pd
    # Normaliza las palabras clave, eliminando espacios adicionales y puntos al final de cada palabra.
    def normalizar(texto):
        texto = re.sub(r"\s+", " ", texto)
        palabras = (p.strip().rstrip(".") for p in texto.split(","))
        return ", ".join(p for p in palabras if p)
    
    # Expresión regular para identificar el inicio de un nuevo cluster y extraer sus datos.
    patron_inicio_cluster = re.compile(r"^\s*(\d+)\s+(\d+)\s+([\d,]+\s*%)\s+(.*)")

    # Carga el archivo
    with open("files/input/clusters_report.txt", encoding="utf-8") as file:
        lines = file.readlines()

    registros = [] # Lista para almacenar los registros de cada cluster.
    actual = None # Diccionario para almacenar los datos del cluster actual mientras se procesa.

    for line in lines:
        line = line.rstrip()
        # Ignora los ecabezados y separadores del reporte.
        if (not line or line.startswith("Cluster") or line.startswith("-") or line.startswith("         palabras")):
            continue

        m = patron_inicio_cluster.match(line)

        if m:
            # Tomamos las palabras clave del cluster anterior antes de iniciar uno nuevo.
            if actual is not None:
                actual["principales_palabras_clave"] = normalizar(actual["principales_palabras_clave"])
                registros.append(actual)

            actual = {
                "cluster": int(m.group(1)), # El número del cluster.
                "cantidad_de_palabras_clave": int(m.group(2)),
                # Porcentaje de palabras clave con formato ajustado
                "porcentaje_de_palabras_clave": float(m.group(3).replace("%", "").replace(",", ".").strip()),
                "principales_palabras_clave": m.group(4).strip(),
            }
        else:
            actual["principales_palabras_clave"] += " " + line.strip()
    # Agrega el último cluster después de procesar todas las líneas.
    if actual is not None:
        actual["principales_palabras_clave"] = normalizar(actual["principales_palabras_clave"])
        registros.append(actual)

    return pd.DataFrame(registros)