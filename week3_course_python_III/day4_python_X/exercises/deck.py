suits = ['Spades', 'Clubs', 'Hearts', 'Diamonds']

def create_suit(suit):
    l = []
    values = ['Ace', '2', '3', '4', '5', '6', '7', '8', '9', 'Jack', 'Queen', 'King']
    for v in values:
        l.append(v + ' of ' + suit)
    return l

def create_deck(lista):
    deck = []
    i = 0
    while i < len(lista):
        deck += create_suit(lista[i])
        i += 1
    return deck

if __name__ == '__main__':
    print(create_deck(suits))