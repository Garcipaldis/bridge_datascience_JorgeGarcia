def display_chessboard(n):
    print(' _ _ _ _ _ _ _ _')
    for i in range(n):
        print('|_' * n + '|')

if '__main__' == __name__:
    display_chessboard(8)