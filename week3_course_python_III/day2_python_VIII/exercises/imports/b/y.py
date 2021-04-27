import os, sys

ruta = __file__
for i in range(2):
    ruta = os.path.dirname(ruta)

sys.path.append(ruta)

import a.x as x

y = 4
b = 16

def f1y(a):
    print('Entrando en f1y')
    return a * x.f1x(x.x, x.a)

def f2y(b):
    print('Entrando en f2y')
    return b ** 2

if __name__ == '__main__':
    print(f1y(y))
    print(f2y(y))