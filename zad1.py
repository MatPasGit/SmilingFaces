import numpy as np
from RandomNumberGenerator import RandomNumberGenerator
import math

def main():
    seed = 20           #ziarno
    n = 4               #liczba zadań

    #Zmienne przechowujące wylosowane dane
    tablep = []
    tablep = [[0 for j in range(n)] for i in range(3)]
    tabled = []
    tabled = [0 for j in range(n)]


    #Generacja instancji
    x = RandomNumberGenerator(20)
    A = 0
    for i in range(3):
        for j in range(n):
            p = x.nextInt(1, 99)
            tablep[i][j] = p
            A = A + p
    B = math.floor(0.5*A)
    A = math.floor((1/6)*A)

    for j in range(n):
        d = x.nextInt(A, B)
        tabled[j] = d





main()
