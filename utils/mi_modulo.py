import os, sys
import random
import itertools
import json
import requests
import time
import numpy as np
import pandas as pd

# Data Wrangling

def omdb_to_csv(ruta, row_start, row_num=1000, key='7b2c6fff'):
    """Función para obtener dataframes de la API de OMDb, destinada a la recolección de datos sobre pelícluas/series según IMDb.
        - Args:
            - ruta: Ruta del fichero csv donde se obtienen las IDs de IMDb.
            - row_start: fila por la que se comienza a realizar peticiones a la API.
            - row_num: número de filas a partir de row_start por las que se realiza la petición. Por defecto 1000.
            - key: La clave para acceder a la API. Personal de cada usuario.
        -Returns:
            - Dataframe con los datos obtenidos.
    """
    movies = pd.read_csv(ruta)
    data = []
    count = 1
    for titleid in movies.loc[row_start:(row_start+row_num), 'titleId']:
        omdb_url = f'http://www.omdbapi.com/?i={titleid}&apikey={key}'
        r = requests.get(omdb_url, params={'plot':'full'}).json()
        time.sleep(0.5)
        print(count)
        count += 1
    df = pd.DataFrame(data)
    df.to_csv(f'Data_OMDb_{row_start}.csv')
    return df

def combined_to_list(path):
    """ Función que transforma los ficheros 'combined' de Netflix para poder tratarlos posteriormente.
        - Args:
            - path: ruta donde se encuentra el fichero 'combined_data_x.txt'.
        - Returns:
            - lista de diccionarios.
    """
    with open(path, 'r') as raw:
        text = raw.readlines()
    res = []
    k = []
    for line in text:
        if ':' not in line:
            res.append(k + line.strip('\n').split(','))
        else:
            k = [line.strip(':\n')]
    return res

def combined_to_csv(path, num=0):
    """ Funcion que transforma los ficheros 'combined' de Netflix a un dataframe. Emplea la función 'combined_to_list'.
        - Args:
            - path: ruta donde se encuentra el fichero 'combined_data_x.txt'.
            - num: número del fichero combined.
        - Returns:
            - Dataframe.
    """
    lista = combined_to_list(path)
    df = pd.DataFrame(lista, columns=['netflix_id', 'user_id', 'rating', 'date'])
    df.to_csv(f'data/Net_combined_{num}.csv')
    return df

# Directorios

def add_path(num):
    '''Función guardada para poder importar módulos desde otros .py (os.getcwd() si es ipynb).
    Args:
        - num: indica el número de veces que se va a obtener la ruta superior.
    '''
    ruta = __file__ # en caso de jupyter se usa os.getcwd()
    for i in range(num):
        ruta = os.path.dirname(ruta)
    sys.path.append(ruta)

# Funciones útiles para Numpy

def filtra_array(funcion, array):
    '''Devuelve una lista filtrada de un array de numpy.
    Args:
        - funcion: cualquier función de un argumento.
        - array: array de una dimensión.
    Returns:
        - Lista filtrada.
    '''
    return list(filter(funcion, list(array)))



# Funciones que conciernen a comandos del sistema operativo

def borrar_pantalla():
    '''Función destinada a borrar la pantalla de la terminal. Muy útil para programas que actualicen datos por pantalla.
    '''
    if os.name == 'posix':
        os.system ('clear')
    elif os.name == 'ce' or os.name == 'nt' or os.name == 'dos':
        os.system ('cls')

def copiar_texto(cadena):
    '''Función para copiar texto en el portapapeles del sistema.
    Args:
        - cadena: String que se copiará.
    '''
    comando = 'echo ' + cadena.strip() + '| clip'
    os.system(comando)

################################################################################################################################
# CLASE de CODIFICACIÓN realizado como un proyecto anterior. Lo incluyo porque me ha resultado útil para contraseñas sencillas.
################################################################################################################################

#Estas funciones no las he desarrollado durante el curso pero considero que me pueden resultar útiles en un futuro.

def genera_rotor():
    '''Utilizada para cambiar las variables de la clase enigmalite
    '''
    letras = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789xcpqe ?!'
    rango = range(len(letras))
    aleatorio = random.sample(rango, len(letras))
    lista_letras = [letras[aleatorio[n]] for n in rango]
    rotor = ''.join(lista_letras)
    return rotor

class enigmalite:
    '''Clase básica que ofrece una codificación/decodificación sencilla
    en cuanto a variables se refiere.
    Las variables son las siguientes:
        - S: Se trata del abecedario(+números y carac. especiales) con
            los pares de letras del Steckerverbindungen implementadas.
        - R1, R2, R3: Son los rotores seleccionados y posicionados.
        - Se incluye un diccionario para los caracteres especiales.
        '''

    S = 'GIEDCZAWBJTLMSUQPRNKOVHYXFxcpqe0123456789'
    especiales = {'x': ' ', 'c': ',', 'p': '.', 'q': '?', 'e': '!'}
    elegidos = {
        'R1': 'qACZO1EHYN7pB2SIx9JLKG3MeV8FUPQW0T4cD5XR6',
        'R2': 'GZH43LPp6c1Aq5JQVexKMUISNRFYBE2COWX9D8T07',
        'R3': 'NGKCIT6qQ3BAHXF180eYD4MLJPU52EVWOc7Rx9pZS',
        'S': 'GIEDCZAWBJTLMSUQPRNKOVHYXFxcpqe0123456789'
        }

    def pasar_por_rotor(self, entrada, R, letra=False, primero=False):
        '''Función que simula el paso de una letra por un rotor específico.
        Se ha empleado la función cycle de itertools para evitar un IndexError
        producido por el paso y el turnover (ambos reflejados en la variable "cuenta".
        '''
        cuenta = 0
        salida = []
        for n in entrada:
            ciclador = itertools.cycle(R)
            for i in range(n + cuenta):
                next(ciclador)
            salida.append(R.index(next(ciclador)))
            if letra and R[n] == letra:
                cuenta += 2
            else:
                if primero:
                    cuenta += 1
        return salida

    def codificar(self, cadena, espacios=True):
        '''Función la cual puede ser dividida en tres partes más simplificadas.
        No se han definido estas partes por separado pues o son muy simples o
        no se emplean en otro lugar.
        La primera parte se encarga de sustituir los caracteres de la cadena
        introducida por aquellos que figuran en S y en el dict de especiales.
        '''
        caracteres = list(cadena)
        entrada = []
        for i in range(len(caracteres)):
            check = False
            for clave, valor in enigmalite.especiales.items():
                if cadena[i] == valor:
                    entrada.append(enigmalite.S.index(clave))
                    check = True
                    break
            if check == False:
                entrada.append(enigmalite.S.index(caracteres[i].upper()))

        '''Esta segunda parte se basa en una concatenación de la función "pasar_por_rotor"
        definida previamente. Esto simula el paso de cada caracter por el teclado modificado
        y los tres rotores.'''
        Sx = self.pasar_por_rotor(entrada, enigmalite.elegidos['S'], primero=True)
        R1x = self.pasar_por_rotor(Sx, enigmalite.elegidos['R1'], letra='R')
        R2x = self.pasar_por_rotor(R1x, enigmalite.elegidos['R2'], letra='F')
        R3x = self.pasar_por_rotor(R2x, enigmalite.elegidos['R3'], letra= 'W')

        '''En la tercera y última parte se procede a presentar la lista final
        en un formato que emule la presentación empleada en los mensajes de la
        máquina. Esto también ayuda a no reconocer las palabras por longitud.'''
        caracteres = [enigmalite.elegidos['R3'][n] for n in R3x]
        if espacios:
            cuarteto = ''
            lista_cuartetos = []
            for i in range(len(caracteres)):
                if len(cuarteto) == 4:
                    lista_cuartetos.append(cuarteto)
                    cuarteto = caracteres[i]
                    if i == len(caracteres) - 1:
                        lista_cuartetos.append(cuarteto)
                elif i == len(caracteres) - 1:
                    cuarteto += caracteres[i]
                    lista_cuartetos.append(cuarteto)
                else:
                    cuarteto += caracteres[i]
            salida = ' '.join(lista_cuartetos)
        else:
            salida = ''.join(caracteres)
        return salida

    def reflejar_rotor(self, entrada, R, letra=False, primero=False):
        '''Función que emula la función del Reflector y que consiste en la inversa
        de la función "pasar_por_rotor". Debido a la naturaleza de la codificación,
        existe un paso en el que se emplea esa misma función para realizar una comprobación
        de que el proceso de decodificación sigue el camino correcto.
        '''
        cuenta_P = 0
        cuenta = 0
        salida_R = []
        for i in range(1, len(entrada) + 1):
            salida_R.append(entrada[i - 1])
            salida_R[i - 1] -= (cuenta + cuenta_P)
            if primero:
                cuenta_P += 1
            if (salida_R[i - 1]) < 0:
                salida_R[i - 1] += len(R) * (1 + abs(salida_R[i - 1]) // (len(R) + 1))
            if cuenta >= 2 * len(entrada):
                break
            elif self.pasar_por_rotor(salida_R, R, letra, primero=primero) == entrada[:i]:
                continue
            elif (salida_R[i - 1] - 2) < 0:
                salida_R[i - 1] += len(R) - 2
                cuenta += 2
            else:
                salida_R[i - 1] -= 2
                cuenta += 2
        return salida_R

    def decodificar(self, cadena):
        '''Función que también puede ser dividida en tres partes.
        La primera revierte la presentación y lo convierte en una lista,
        la segunda nuevamente una concatenación y la tercera una presentación
        casi idéntica al formato original. Se define como "idéntico" y no "exacto"
        por cuestión de mayúsculas en los nombres propios.
        '''
        # Conversión
        lista_palabras = list(''.join(cadena.split(' ')))
        entrada = [enigmalite.elegidos['R3'].index(lista_palabras[i]) for i in range(len(lista_palabras))]

        # Concatenación
        X3 = self.reflejar_rotor(entrada, enigmalite.elegidos['R3'], letra='W')
        X2 = self.reflejar_rotor(X3, enigmalite.elegidos['R2'], letra='F')
        X1 = self.reflejar_rotor(X2,enigmalite.elegidos['R1'], letra='R')
        XS = self.reflejar_rotor(X1, enigmalite.elegidos['S'], primero=True)

        # Presentación
        caracteres_S = [enigmalite.elegidos['S'][i] for i in XS]
        lista_letras = []
        for n in range(len(caracteres_S)):
            if caracteres_S[n] in enigmalite.especiales.keys():
                lista_letras.append(enigmalite.especiales[caracteres_S[n]])
            elif n != 0 and n != 1 and n != len(caracteres_S) - 1 and caracteres_S[n - 2] == 'p':
                lista_letras.append(caracteres_S[n])
            elif n == 0:
                lista_letras.append(caracteres_S[n])
            else:
                lista_letras.append(caracteres_S[n].lower())

        cadena = ''.join(lista_letras)
        return cadena


if __name__ == '__main__':
    e = enigmalite()
    entrada = input('Introducir password a codificar/decodificar:')
    print(e.decodificar(entrada))