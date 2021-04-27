import os, sys

ruta = __file__
for i in range(3):
    ruta = os.path.dirname(ruta)

sys.path.append(ruta)

import a.x as x
import b.y as y

z = 3
c = 9

def f1z():
    print('Entrando en f1z')
    return y.f1y(z) // c

def f2z():
    print('Entrando en f2z')
    return x.f2x(z, c)

if __name__ == '__main__':
    print(f1z())
    print(f2z())