


class Tablero:

    def __init__(self, dic=None):
        if dic:
            self.dic = dic
        else:
            self.dic = {n:{i:'~' for i range(n,n+10)} for n in range(10)}