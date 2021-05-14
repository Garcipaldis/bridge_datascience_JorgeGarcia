# HUNDIR LA FLOTA

import random

######################################################################################################################################
# VARIABLES
BARCOS = [2, 2, 2, 2, 3, 3, 3, 4, 4, 5]

######################################################################################################################################
# CLASES
class Tablero:
    """Clase Tablero que interactúa tanto con el usuario como con las instancias de la clase Ship.
    """

    def __init__(self, dic=None):
        """Contructor que por defecto genera un diccionario de coordenadas en blanco.

            - Args: dic=None: Si no se aporta un diccionario de coordenadas se asignará a self.dic uno en blanco.

            - Attributes:
                    - self.init: Diccionario de coordenadas que no mostrará los barcos añadidos al usuario.
                    - self.dic: Diccionario de coordenadas que muestra los barcos.
                    - self.ships: Lista donde se añadirán las instancias de la clase Ship.

        """
        self.init = {n:{i:'~' for i in range(10)} for n in range(10)}
        self.ships = []
        if dic:
            self.dic = dic
        else:
            self.dic = {n:{i:'~' for i in range(10)} for n in range(10)}

    def display_tablero(self, blank=False):
        """ Método que muestra por pantalla el tablero.
            - Args: blank=False: Por defecto muestra por pantalla self.dic, que contiene los barcos.
                    Si se cambia a True mostrará self.init (Tablero en blanco).
        """
        print('x',0,1,2,3,4,5,6,7,8,9)
        if blank:
            for k, d in self.init.items():
                print(k,d[0],d[1],d[2],d[3],d[4],d[5],d[6],d[7],d[8],d[9])
        else:
            for k, d in self.dic.items():
                print(k,d[0],d[1],d[2],d[3],d[4],d[5],d[6],d[7],d[8],d[9])

    def check_pos(self, x, y, size, orientacion):
        """Método que comprueba si el barco que se va a insertar se halla dentro de los límites del Tablero.
            - Args:
                - x: Fila x
                - y: Columna y
                - size: Tamaño del barco
                - orientacion: Toma valores ['N', 'S', 'O', 'E'] representando los ejes cardinales.
            - Returns:
                - True/False: Si cumple que se encuentra dentro del Tablero o no.
        """
        if orientacion == 'N' and x > size:
            return True
        elif orientacion == 'S' and (9 - x) > size:
            return True
        elif orientacion == 'O' and y > size:
            return True
        elif orientacion == 'E' and (9 - y) > size:
            return True
        else:
            return False
    
    def to_coordinates(self, x, y, size, orientacion):
        """ Método que transforma los atributos de la instancia de Ship en una lista de coordenadas.
            - Args:
                - x: Fila x
                - y: Columna y
                - size: Tamaño del barco
                - orientacion: Toma valores ['N', 'S', 'O', 'E'] representando los ejes cardinales.
            -Returns:
                - Lista de coordenadas.
        """
        coordenadas = [(x, y)]
        for n in range(size-1):
            if orientacion == 'N':
                x -= 1
                coordenadas.append((x,y))
            elif orientacion == 'S':
                x += 1
                coordenadas.append((x,y))
            elif orientacion == 'E':
                y += 1
                coordenadas.append((x,y))
            if orientacion == 'O':
                y -= 1
                coordenadas.append((x,y))
        return coordenadas

    def check_ship(self, x, y, size, orientacion):
        """Método que comprueba si el barco que se va a insertar NO se solapa con otro barco ya insertado..
            - Args:
                - x: Fila x
                - y: Columna y
                - size: Tamaño del barco
                - orientacion: Toma valores ['N', 'S', 'O', 'E'] representando los ejes cardinales.
            - Returns:
                - True/False: Si cumple que NO se solapa con ningún barco.
        """
        coordenadas = self.to_coordinates(x, y, size, orientacion)
        for c in coordenadas:
            if self.dic[c[0]][c[1]] == '#':
                return False
        return True

    def total_check(self, barco):
        """ Método que combina check_pos y check_ship.
            - Args: barco: Instancia de la clase Ship.
            - Returns: True/False en función de ambas comprobaciones.
        """
        x, y = barco.fila_x, barco.columna_y
        size = barco.size
        orientacion = barco.orientacion
        if self.check_pos(x, y, size, orientacion) and self.check_ship(x, y, size, orientacion):
            return True
        else:
            return False


    def add_ship(self, barco, display=False):
        """ Método que añade las coordenadas asociadas a una instancia de Ship al diccionario self.dic.
            Además, añade la instancia a la lista self.Ships.
            - Args: barco: Instancia de la clase Ship.
        """
        if self.total_check(barco) == False:
            return False
        fila, columna = barco.fila_x, barco.columna_y
        for l in range(barco.size):
            self.dic[fila][columna] = '#'
            if barco.orientacion == 'N':
                fila -= 1
            elif barco.orientacion == 'S':
                fila += 1
            elif barco.orientacion == 'O':
                columna -= 1
            else:
                columna += 1
        self.ships.append(barco)
        if display:
            self.display_tablero()
        return True

    def update_ship(self, barco, x, y):
        """ Método que actualiza los diccionarios self.init y self.dic cuando un barco es alcanzado en una coordenadas determinada.
        Además llama también al método update_vida de la instancia de Ship.
            - Args:
                - barco: Instancia de la clase Ship.
                - x: fila x
                - y: columna y
            -Returns:
                - 'Tocado y hundido': Cuando el valor devuelto por update_vida == 0.
                - 'Tocado': Cuando el valor devuelto por update_vida > 0.
        """
        vida = barco.update_vida()
        if vida == 0:
            self.dic[x][y] = 'X'
            self.init[x][y] = 'X'
            self.ships.remove(barco)
            return f'Tocado y hundido. Quedan {len(self.ships)} barcos.'
        elif vida > 0:
            self.dic[x][y] = 'X'
            self.init[x][y] = 'X'
            return 'Tocado'

    def find_ship(self, x, y):
        """ Método que busca un barco en self.Ships que contenga las coordenadas insertadas.
            - Args:
                - x: fila x
                - y: columna y
            - Returns:
                - Instancia concreta de la clase Ship contenida en self.Ships
        """
        for ship in self.ships:
            coordenadas = self.to_coordinates(ship.fila_x, ship.columna_y, ship.size, ship.orientacion)
            if (x, y) in coordenadas:
                return ship

    def shoot(self, x, y):
        """Método que comprueba si las coordenadas insertadas pertenecen a un barco y toma las acciones necesarias.
            - Args:
                - x: fila x
                - y: columna y
            - Returns:
                - Tocado/Tocado y hundido: Si se acertó a un barco.
                - Agua: Si no se acertó a ningún barco.
        """
        if self.dic[x][y] == '#':
            ship = self.find_ship(x, y)
            return self.update_ship(ship, x, y)
        else:
            self.dic[x][y] = 'O'
            self.init[x][y] = 'O'
            return 'Agua'


class Ship:
    """ Clase que representa cada uno de los barcos de la partida.
    """

    def __init__(self, size, fila_x, columna_y, orientacion):
        """ Constructor que toma los valores necesarios para obtener una instancia.
            - Args:
                - size: Tamaño del barco. Esto determinará también el valor de su atributo self.vida
                - fila_x: Valor de la coordenada x como punto de referencia.
                - columna_y: Valor de la coordenada y como punto de referencia.
                - orientacion: Toma valores ['N', 'S', 'O', 'E'] representando los ejes cardinales.
        """
        self.size = size
        self.fila_x = fila_x
        self.columna_y = columna_y
        self.orientacion = orientacion
        self.vida = size

    def update_vida(self):
        """ Método que modifica la vida del barco en uno cada vez que se llama.
            - Returns: El valor de la vida del barco.
        """
        self.vida -= 1
        return self.vida

######################################################################################################################################
# FUNCIONES
def ask_ship(i, num, tablero):
    """ Función que pide al usuario introducir los valores necesarios para añadir un barco al tablero.
        - Args:
            - i: índice para mostar al usuario el número de barco.
            - num: tamaño del barco.
            - tablero: instancia de la clase Tablero.
        -Returns:
            - True/False: En función de si se ha introducido STOP o si se han añadido todos los barcos.
    """
    name = f'S_{num}_{i}'
    size = num
    while True:
        try:
            x = int(input(f'Introduzca coordenada x para barco {num}x1 número {i}: '))
            y = int(input(f'Introduzca coordenada y para barco {num}x1 número {i}: '))
        except ValueError:
            print('Introduzca coordenadas válidas.')
            continue
        orientacion = input(f'Introduzca orientacion (N, S, E, O) y para barco {num}x1 número {i} [STOP para detener]: ').upper()
        if orientacion == 'STOP':
            return False
        elif orientacion not in ['N', 'S', 'E', 'O']:
            print('Introduzca una orientación válida (N, S, O, E)')
            continue
        name = Ship(size, x, y, orientacion)
        if tablero.add_ship(name) == False:
            print('El barco introducido no se encuentra en los límites del tablero o solapa a otro barco. Por favor introduzca otros valores.')
            continue
        return True

def set_game(lista, tablero):
    """ Función que llama a ask_ship por cada valor de una lista.
        - Args:
            - lista: lista de valores con el temaño de cada barco.
            - tablero: instancia de la clase tablero.
        - Returns:
            - True/False: En función de si se han introducido todos los barcos o si se ha parado el proceso.
    """
    for i, v in enumerate(lista):
        if ask_ship(i, v, tablero) == False:
            return False
    return True

def set_random_game(lista, tablero):
    placed = 0
    while placed < len(lista):
        name = f'B{placed}'
        size = lista[placed]
        x = random.randint(0,9)
        y = random.randint(0,9)
        orientacion = random.sample(['N', 'S', 'O', 'E'],1)[0]
        name = Ship(size, x, y, orientacion)
        if tablero.add_ship(name):
            placed += 1

def shoot(tablero):
    while True:
        try:
            x = int(input(f'Coordenada x: '))
            y = int(input(f'Coordenada y: '))
        except ValueError:
            print('Introduzca coordenadas válidas.')
            continue
        if x == 'STOP' or y == 'STOP':
            return False
        print(tablero.shoot(int(x), int(y)))
        tablero.display_tablero(blank=True)
        return True

def play(tablero):
    print('Total Ships:', len(tablero.ships))
    vidas = sum([barco.vida for barco in tablero.ships])
    contador = 1
    while vidas > 0:
        print(f'Turno {contador}:')
        print('='*10)
        shoot(tablero)
        contador += 1
    print('¡Has ganado!')

def main(lista, random=True):
    t = Tablero()
    if random:
        set_random_game(lista, t)
        play(t)
    else:
        if set_game(lista, t):
            play(t)

if __name__ == '__main__':
    main(BARCOS)
    """t = Tablero()
    b = Ship(2, 0, 0, 'O')
    print(t.check_pos(9, 9, 2, 'O'))
    print(t.check_pos(9, 9, 2, 'E'))
    print(t.check_pos(9, 9, 2, 'N'))
    print(t.check_pos(9, 9, 2, 'S'))
    """