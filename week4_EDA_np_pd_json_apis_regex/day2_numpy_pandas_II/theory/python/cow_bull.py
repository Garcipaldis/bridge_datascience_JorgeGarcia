import random 

def cow_bull():
    # Un número es generado de manera aleatoria
    generated_num = str(random.randint(1000,9999))

    acum_cows = 0
    guess_str =""
    while acum_cows < 4 and guess_str != "STOP":
        # los acumuladores se inicializan con cada iteración
        acum_cows = 0
        acum_bulls = 0

        guess_str = input("Please enter a number between 1000 and 9999 (STOP to stop): ")
        print(f"Your number {guess_str}")
        # variable auxiliar para poder modificar los dígitos si se encuentran vacas
        generated_num_cowed = list(generated_num) 

        # En el primer recorrido del bucle, se obtienen los números que coinciden y se sustituyen los dígitos por una 'c' para no ser contabilizados en la búsqueda de toros
        for i, item in enumerate (generated_num):
            if item == guess_str[i]:
                acum_cows += 1
                generated_num_cowed[i] = "c"

        # En el segundo recorrido, se obtien los números que están pero no coinciden
        for i in range(len(generated_num_cowed)):
            for j in range(len(guess_str)):
                    if guess_str[i] == generated_num_cowed[j]:
                        acum_bulls += 1


        print(f"{acum_cows} cows, {acum_bulls} bulls.")

if __name__ == '__main__':
    cow_bull()