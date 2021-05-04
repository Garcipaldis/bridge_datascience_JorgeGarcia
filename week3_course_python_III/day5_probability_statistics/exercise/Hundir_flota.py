


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

    def add_ship(self, barco):
        # TODO actualizar una vez se especifique el método de entrada de coordenadas.
        start = barco.start
        fila, columna = int(start[0]), int(start[1])
        for l in range(barco.size):
            self.dic[fila][columna] = '#'
            if barco.orientacion == 'v':
                fila += 1
            else:
                columna += 1
        self.ships.append(barco)

    def check(self, coordenada):
        # TODO a la espera de especificación del método de entrada de coordenadas. 
        for barco in self.ships:
            coor = [barco.start.split()]
            for i in range(barco.size):
                if barco.orientacion == 'v':
                    coor.append([str(int(coor[0][0])+i+1), coor[0][1]])
                else:
                    coor.append([coor[0][0], str(int(coor[0][1]+i+1))])
            if coordenada.split() in coor:
                return True
        return False

    def update_ship(self, barco, coordenada):
        pass

    def shoot(self, coordenada):
        # TODO a la espera de especificación del método de entrada de coordenadas.
        pass


class Barco:

    def __init__(self, size, orientacion, start):
        self.size = size
        self.vida = size
        self.orientacion = orientacion
        self.start = start

    def update_salud(self, coordenada):
        pass



if __name__ == '__main__':
    t = Tablero()
    b = Barco(3, 'v', '22')
    t.add_ship(b)
    t.display_tablero()
    print(t.ships[0].vida)