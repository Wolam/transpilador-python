# Manejar los archivos .cm

def cargar_archivo(ruta) -> str:
    """
    Carga una ruta de archivo y retorna
    el contenido del archivo.
    """
    with open(ruta, "r") as archivo:
        contenido = archivo.read()
    return contenido
