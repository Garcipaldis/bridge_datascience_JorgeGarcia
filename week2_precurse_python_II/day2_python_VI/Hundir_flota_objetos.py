import pandas as pd


class Tablero:

    def __init__(self):
        self.matrix = self.matrix_creator()

    def matrix_creator(self):
        index = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
        d = {}
        d2 = {}

        for i in index:
            for j in range(1, len(index) + 1):
                d2[j] = '~'
            d[i] = d2

        df = pd.DataFrame(d)
        df = df.T
        return df

class Ship:

    def __init__(self, size, initial_point, alignment):
        self.size = size
        self.initial_point = initial_point
        self.alignment = alignment

    def modify_life(self):
        pass

    