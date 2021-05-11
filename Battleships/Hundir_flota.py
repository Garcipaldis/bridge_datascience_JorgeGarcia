#VARIABLES

ORIENTATIONS = ("N", "S", "E", "O") 
DIMENSIONES = (10,10)
BARCOS = {
    "barco_1_1": 1,
    "barco_1_2": 1,
    "barco_1_3": 1,
    "barco_1_4": 1,
    "barco_2_1": 2,
    "barco_2_2": 2,
    "barco_2_3": 2,
    "barco_3_1": 3,
    "barco_3_2": 3,
    "barco_4_1": 4,
}

CLAVES = {
    "boat": "O",
    "water": " ",
    "hit": "X",
    "fail": "-"
}


class Tablero:

    def __init__(self, dic=None):
        self.ships = []
        if dic:
            self.dic = dic
        else:
            self.dic = {n:{i:'~' for i in range(10)} for n in range(10)}

    def display_tablero(self):
        print('x',0,1,2,3,4,5,6,7,8,9)
        for k, d in self.dic.items():
            print(k,d[0],d[1],d[2],d[3],d[4],d[5],d[6],d[7],d[8],d[9])

    def check_pos(self, x, y, size, orientacion):
        if orientacion == 'N' and x < size:
            return True
        elif orientacion == 'S' and (9 - x) > size:
            return True
        elif orientacion == 'O' and y < size:
            return True
        elif orientacion == 'E' and (9 - y) > size:
            return True
        else:
            return False
    
    def to_coordinates(self, x, y, size, orientacion):
        coordenadas = [(x, y)]
        for n in range(size):
            if orientacion == 'N':
                x -= 1
                coordenadas.append((x,y))
            elif orientacion == 'S':
                x += 1
                coordenadas.append((x,y))
            elif orientacion == 'E':
                y += 1
                coordenadas.append((x,y))
            if orientacion == 'N':
                y -= 1
                coordenadas.append((x,y))
        return coordenadas

    def check_ship(self, x, y, size, orientacion):
        coordenadas = self.to_coordinates(x, y, size, orientacion)
        for c in coordenadas:
            if self.dic[c[0]][c[1]] == '#':
                return False
        return True

    def total_check(self, barco):
        x, y = barco.fila_x, barco.columna_y
        size = barco.size
        orientacion = barco.orientacion
        if self.check_pos(x, y, size, orientacion) and self.check_ship(x, y, size, orientacion):
            return True
        else:
            return False


    def add_ship(self, barco):
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

    def check(self, x, y):
        pass

    def check_orginal(self, x, y):
        # TODO a la espera de especificación del método de entrada de coordenadas. 
        for barco in self.ships:
            coor = [(barco.fila_x, barco.columna_y)]
            for i in range(barco.size):
                if barco.orientacion == 'N':
                    coor.append([str(int(coor[0][0])+i+1), coor[0][1]])
                else:
                    coor.append([coor[0][0], str(int(coor[0][1]+i+1))])
            if (x,y) in coor:
                return True
        return False

    def update_ship(self, barco, x, y):
        pass

    def shoot(self, x, y):
        if self.dic[x][y] == '#':
            return True
        else:
            return False


class Ship:

    def __init__(self, size, fila_x, columna_y, orientacion):
        self.size=size
        self.fila_x = fila_x
        self.columna_y = columna_y
        self.orientacion = orientacion
        self.vida = [True for i in range(size)]

    def update_vida(x, y):
        pass
'''
disparo_fila =()
disparo_columna =()
all_ships = ()


    for ship in all_ships:
                if disparo_fila == ship(fila_x) and disparo_columna == ship(columna_y):
                    print (Tocado !!!)
                if len(ship) == 0:

                if all_ships.index(ship) == 0:
                        print "Has hundido el barco..."
                        break
                elif all_ships.index(ship) == 1:
                        print "Has hundido el barco..."
                        break
                elif all_ships.index(ship) == 2:
                        print "Has hundido el barco..."
                        break
                elif all_ships.index(ship) == 3:
                        print "Has hundido el barco..."
                        break
                elif all_ships.index(ship) == 4:
                        print "Has hundido el barco..."
                        break

                elif  len(all_ships) == 0:
                        print "Has ganado!"
                        '''


if __name__ == '__main__':
    t = Tablero()
    b = Ship(3, 2, 2, 'S')
    b2 = Ship(3, 2, 4, 'E')
    t.add_ship(b)
    t.add_ship(b2)
    t.display_tablero()
    print(t.ships)

    coordenadas = [(2,2), (2,3), (2,4)]