class Humano:

    def __init__(self, nombre, armadura, nivel, ataque, salud=100, ojos=2, piernas=2, dientes=32):
        self.nombre = nombre
        self.armadura = armadura
        self.nivel = nivel
        self.ataque = ataque
        self.salud = salud
        self.ojos = ojos
        self.piernas = piernas
        self.dientes = dientes

    def atacar(self, orco):
        resta = self.ataque - orco.armadura
        orco.salud -= resta
        print(orco.salud)

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
    a = Humano('Aragorn', 30, 50, 20)
    a.muestra_atributos()
