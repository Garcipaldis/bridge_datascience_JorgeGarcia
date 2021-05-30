import os, sys
import json

def read_json(fullpath):
    with open(fullpath, "r") as json_file_readed:
        json_readed = json.load(json_file_readed)
    return json_readed

def add_path(num, jupyter=True):
    '''Función guardada para poder importar módulos desde otros .py (os.getcwd() si es ipynb).
    Args:
        - num: indica el número de veces que se va a obtener la ruta superior.
    '''
    if jupyter:
        dirpath = os.getcwd()
    else:
        dirpath = __file__ # en caso de jupyter se usa os.getcwd()
    for i in range(num):
        dirpath = os.path.dirname(dirpath)
    sys.path.append(dirpath)

    return dirpath