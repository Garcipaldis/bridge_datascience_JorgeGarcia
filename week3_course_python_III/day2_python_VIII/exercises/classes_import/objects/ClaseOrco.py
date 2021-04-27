class Orco:

    def __init__(self, nombre, armadura, nivel, ataque, salud=100, ojos=2, piernas=2, dientes=56):
        self.nombre = nombre
        self.armadura = armadura
        self.nivel = nivel
        self.ataque = ataque
        self.salud = salud
        self.ojos = ojos
        self.piernas = piernas
        self.dientes = dientes

    def atacar(self, humano):
        resta = self.ataque - humano.armadura
        humano.salud -= resta
        print(humano.salud)

    def no_vivo(self):
        if self.salud <= 0:
            return True
        else:
            return False

    def muestra_atributos(self):
        salida = ''
        for k in self.__dict__.keys():
            salida += str(k) + ' : ' + str(self.__dict__[k]) + ' | '
        print(salida)

if __name__ == '__main__':
    import ClaseHumano as ch

    a = ch.Humano('Aragorn', 5, 50, 20)
    g = Orco('Garrosh', 10, 40, 15)

    a.atacar(g)