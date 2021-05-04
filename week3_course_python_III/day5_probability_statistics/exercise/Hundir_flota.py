


class Tablero:

    def __init__(self, dic=None):
        if dic:
            self.dic = dic
        else:
            self.dic = {n:{i:'~' for i in range(10)} for n in range(10)}

    def display_tablero(self):
        for d in self.dic.values():
            print(d[0],d[1],d[2],d[3],d[4],d[5],d[6],d[7],d[8],d[9])

    def add_ship(self, barco):
        pass

    def update_ship(self, barco):
        pass


class Barco:

    def __init__(self, size, orientacion, start):
        self.size = size
        self.vida = size
        self.orientacion = orientacion
        self.start = start

    def define_coordenadas(self):
        pass

    def update_salud(self, coordenada):
        pass



if __name__ == '__main__':
    t = Tablero()
    t.display_tablero()