import os, sys
import random
import itertools
import warnings
import requests
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split, RepeatedKFold
from sklearn.preprocessing import PolynomialFeatures

#Cross-Validation
def model_crossval_scores(X, y, model, splits=10, epochs=1, random_state=42, degree=False, plot=True, show_warnings=False):

    if show_warnings == False:
        warnings.filterwarnings('ignore')

    scores = {'Epoch':[],'Iteration':[],'Train_Score':[], 'Val_Score':[]}
    epoch = 1
    iteration = 1

    # Cross Validation Data Collection
    if degree:
        polinominal_model = PolynomialFeatures(degree) 
        X = polinominal_model.fit_transform(X, y)
    rkf = RepeatedKFold(n_splits=splits, n_repeats=epochs, random_state=random_state)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=random_state)

    for train_index, val_index in rkf.split(X_train):

        model.fit(X_train[train_index], y_train[train_index])
        train_score = model.score(X_train[train_index], y_train[train_index])
        val_score = model.score(X_train[val_index], y_train[val_index])

        scores['Train_Score'].append(train_score)
        scores['Val_Score'].append(val_score)
        scores['Iteration'].append(iteration)
        scores['Epoch'].append(epoch)
        
        iteration += 1
        if iteration > splits:
            iteration = 1
            epoch += 1

    # Epoch Plots
    df = pd.DataFrame(scores, index=range(len(scores['Val_Score'])))

    if plot:
        for e in range(1, epochs+1):
            x_plot = df[df.Epoch == e]['Iteration']
            y_plot_train = df[df.Epoch == e]['Train_Score']
            y_plot_val = df[df.Epoch == e]['Val_Score']
            fig, ax = plt.subplots()
            ax.plot(x_plot, y_plot_train, color='green', label='Train Score')
            ax.plot(x_plot, y_plot_val, color='red', label='Val Score')
            if degree:
                plt.title(f'Poly deg:{degree} | Train/Val Score | Epoch: {e}')
            else:
                plt.title(f'{model} | Train/Val Score | Epoch: {e}')
            ax.legend(loc='best')
            plt.show()

    return df

# Columnas mejor correlacionadas en Dataframe.
def get_redundant_pairs(df):
    '''Get diagonal and lower triangular pairs of correlation matrix'''
    pairs = {'Column_A':[], 'Column_B':[]}
    cols = df.columns
    for i in range(0, df.shape[1]):
        for j in range(0, i+1):
            pairs['Column_A'].append(cols[i])
            pairs['Column_B'].append(cols[j])
    return pairs

def get_top_abs_correlations(df, n=5):
    au_corr = df.corr().abs().unstack()
    pairs = get_redundant_pairs(df)
    tuple_pairs = list(zip(pairs['Column_A'], pairs['Column_B']))

    au_corr = au_corr.drop(labels=tuple_pairs).sort_values(ascending=False)
    df = pd.DataFrame(au_corr[0:n], columns=['Correlation'])
    df.reset_index(inplace=True)
    return df

# Data Wrangling

def omdb_to_csv(ruta, row_start, row_num=1000, key='7b2c6fff'):
    """Funci??n para obtener dataframes de la API de OMDb, destinada a la recolecci??n de datos sobre pel??cluas/series seg??n IMDb.
        - Args:
            - ruta: Ruta del fichero csv donde se obtienen las IDs de IMDb.
            - row_start: fila por la que se comienza a realizar peticiones a la API.
            - row_num: n??mero de filas a partir de row_start por las que se realiza la petici??n. Por defecto 1000.
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
    """ Funci??n que transforma los ficheros 'combined' de Netflix para poder tratarlos posteriormente.
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
    """ Funcion que transforma los ficheros 'combined' de Netflix a un dataframe. Emplea la funci??n 'combined_to_list'.
        - Args:
            - path: ruta donde se encuentra el fichero 'combined_data_x.txt'.
            - num: n??mero del fichero combined.
        - Returns:
            - Dataframe.
    """
    lista = combined_to_list(path)
    df = pd.DataFrame(lista, columns=['netflix_id', 'user_id', 'rating', 'date'])
    df.to_csv(f'data/Net_combined_{num}.csv')
    return df

# Directorios

def add_path(num):
    '''Funci??n guardada para poder importar m??dulos desde otros .py (os.getcwd() si es ipynb).
    Args:
        - num: indica el n??mero de veces que se va a obtener la ruta superior.
    '''
    ruta = __file__ # en caso de jupyter se usa os.getcwd()
    for i in range(num):
        ruta = os.path.dirname(ruta)
    sys.path.append(ruta)

# Funciones ??tiles para Numpy

def filtra_array(funcion, array):
    '''Devuelve una lista filtrada de un array de numpy.
    Args:
        - funcion: cualquier funci??n de un argumento.
        - array: array de una dimensi??n.
    Returns:
        - Lista filtrada.
    '''
    return list(filter(funcion, list(array)))



# Funciones que conciernen a comandos del sistema operativo

def borrar_pantalla():
    '''Funci??n destinada a borrar la pantalla de la terminal. Muy ??til para programas que actualicen datos por pantalla.
    '''
    if os.name == 'posix':
        os.system ('clear')
    elif os.name == 'ce' or os.name == 'nt' or os.name == 'dos':
        os.system ('cls')

def copiar_texto(cadena):
    '''Funci??n para copiar texto en el portapapeles del sistema.
    Args:
        - cadena: String que se copiar??.
    '''
    comando = 'echo ' + cadena.strip() + '| clip'
    os.system(comando)

################################################################################################################################
# CLASE de CODIFICACI??N realizado como un proyecto anterior. Lo incluyo porque me ha resultado ??til para contrase??as sencillas.
################################################################################################################################

#Estas funciones no las he desarrollado durante el curso pero considero que me pueden resultar ??tiles en un futuro.

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
    '''Clase b??sica que ofrece una codificaci??n/decodificaci??n sencilla
    en cuanto a variables se refiere.
    Las variables son las siguientes:
        - S: Se trata del abecedario(+n??meros y carac. especiales) con
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
        '''Funci??n que simula el paso de una letra por un rotor espec??fico.
        Se ha empleado la funci??n cycle de itertools para evitar un IndexError
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
        '''Funci??n la cual puede ser dividida en tres partes m??s simplificadas.
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

        '''Esta segunda parte se basa en una concatenaci??n de la funci??n "pasar_por_rotor"
        definida previamente. Esto simula el paso de cada caracter por el teclado modificado
        y los tres rotores.'''
        Sx = self.pasar_por_rotor(entrada, enigmalite.elegidos['S'], primero=True)
        R1x = self.pasar_por_rotor(Sx, enigmalite.elegidos['R1'], letra='R')
        R2x = self.pasar_por_rotor(R1x, enigmalite.elegidos['R2'], letra='F')
        R3x = self.pasar_por_rotor(R2x, enigmalite.elegidos['R3'], letra= 'W')

        '''En la tercera y ??ltima parte se procede a presentar la lista final
        en un formato que emule la presentaci??n empleada en los mensajes de la
        m??quina. Esto tambi??n ayuda a no reconocer las palabras por longitud.'''
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
        '''Funci??n que emula la funci??n del Reflector y que consiste en la inversa
        de la funci??n "pasar_por_rotor". Debido a la naturaleza de la codificaci??n,
        existe un paso en el que se emplea esa misma funci??n para realizar una comprobaci??n
        de que el proceso de decodificaci??n sigue el camino correcto.
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
        '''Funci??n que tambi??n puede ser dividida en tres partes.
        La primera revierte la presentaci??n y lo convierte en una lista,
        la segunda nuevamente una concatenaci??n y la tercera una presentaci??n
        casi id??ntica al formato original. Se define como "id??ntico" y no "exacto"
        por cuesti??n de may??sculas en los nombres propios.
        '''
        # Conversi??n
        lista_palabras = list(''.join(cadena.split(' ')))
        entrada = [enigmalite.elegidos['R3'].index(lista_palabras[i]) for i in range(len(lista_palabras))]

        # Concatenaci??n
        X3 = self.reflejar_rotor(entrada, enigmalite.elegidos['R3'], letra='W')
        X2 = self.reflejar_rotor(X3, enigmalite.elegidos['R2'], letra='F')
        X1 = self.reflejar_rotor(X2,enigmalite.elegidos['R1'], letra='R')
        XS = self.reflejar_rotor(X1, enigmalite.elegidos['S'], primero=True)

        # Presentaci??n
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