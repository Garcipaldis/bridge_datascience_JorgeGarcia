# JUEGO DE HUNDIR LA FLOTA

def ask_players():
    player1 = input('Introduzca nombre del jugador 1:')
    player2 = input('Introduzca nombre del jugador 2:')
    return player1, player2

lista_blanks = [' ' for i in range(100)]

def display(l):
    print('HUNDIR LA FLOTA')
    print('===========================================')
    print('0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |')
    print('-------------------------------------------')
    print(f'1 | {l[0]} | {l[1]} | {l[2]} | {l[3]} | {l[4]} | {l[5]} | {l[6]} | {l[7]} | {l[8]} | {l[9]} |')
    print('-------------------------------------------')
    print(f'2 | {l[10]} | {l[11]} | {l[12]} | {l[13]} | {l[14]} | {l[15]} | {l[16]} | {l[17]} | {l[18]} | {l[19]} |')
    print('-------------------------------------------')
    print(f'3 | {l[20]} | {l[21]} | {l[22]} | {l[23]} | {l[24]} | {l[25]} | {l[26]} | {l[27]} | {l[28]} | {l[29]} |')
    print('-------------------------------------------')
    print(f'4 | {l[30]} | {l[31]} | {l[32]} | {l[33]} | {l[34]} | {l[35]} | {l[36]} | {l[37]} | {l[38]} | {l[39]} |')
    print('-------------------------------------------')
    print(f'5 | {l[40]} | {l[41]} | {l[42]} | {l[43]} | {l[44]} | {l[45]} | {l[46]} | {l[47]} | {l[48]} | {l[49]} |')
    print('-------------------------------------------')
    print(f'6 | {l[50]} | {l[51]} | {l[52]} | {l[53]} | {l[54]} | {l[55]} | {l[56]} | {l[57]} | {l[58]} | {l[59]} |')
    print('-------------------------------------------')
    print(f'7 | {l[60]} | {l[61]} | {l[62]} | {l[63]} | {l[64]} | {l[65]} | {l[66]} | {l[67]} | {l[68]} | {l[69]} |')
    print('-------------------------------------------')
    print(f'8 | {l[70]} | {l[71]} | {l[72]} | {l[73]} | {l[74]} | {l[75]} | {l[76]} | {l[77]} | {l[78]} | {l[79]} |')
    print('-------------------------------------------')
    print(f'9 | {l[80]} | {l[81]} | {l[82]} | {l[83]} | {l[84]} | {l[85]} | {l[86]} | {l[87]} | {l[88]} | {l[89]} |')
    print('-------------------------------------------')
    print(f'10| {l[90]} | {l[91]} | {l[92]} | {l[93]} | {l[94]} | {l[95]} | {l[96]} | {l[97]} | {l[98]} | {l[99]} |')
    print('-------------------------------------------')

barcos = [(60,61), (44,54), (97,98,99)]

def ship_coordinates(ships):
    coordenadas = [' ' for i in range(100)]
    for ship in ships:
        for c in ship:
            coordenadas[c] = '*'
    return coordenadas

horizontales = {1:list(range(10)), 2:list(range(10,20)), 3:list(range(20,30)), 4:list(range(30,40)), 5:list(range(40,50)), 
                6:list(range(50,60)), 7:list(range(60,70)), 8:list(range(70,80)), 9:list(range(80,90)), 10:list(range(90,100))}
verticales = {1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[], 8:[], 9:[], 10:[]}


def ask_ships(num, size):
    barcos = []
    for n in num:
        entrada = input(f'Introduzca posición barco de tamaño {size} (ej. 4h9:10:')
        pass

coordenadas = ship_coordinates(barcos)

display(coordenadas)
