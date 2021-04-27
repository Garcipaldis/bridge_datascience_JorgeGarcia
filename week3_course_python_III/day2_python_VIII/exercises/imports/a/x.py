x = 5
a = 25

def f1x(x, y):
    print('Entrando en f1x')
    return x + y

def f2x(x, y):
    print('Entrando en f2x')
    return x - y


if __name__ == '__main__':
    print(f1x(x, a))
    print(f2x(x, a))