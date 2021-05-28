#Importy
import numpy as np
from RandomNumberGenerator import RandomNumberGenerator
import math
import random
from matplotlib import pyplot as plt

#Zmienne

seed = 20  # ziarno
n = 10  # liczba zadań
maxIter = 100  # maksymalna liczba iteracji
c1 = 1 #współczynnik przy makespan
c2 = 1 #współczynnik przy maxTardiness
c3 = 1 #współćzynnik przy maxTotalTardiness


#DWA PIERWSZE KRYTERIA: 1 (makespan) i 3 (max tardiness)
# Makespan - czas zakończenia wszystkich zadań
# Max tardiness - maksymalne spóźnienie zadania

def takeFirst(elem):
    return elem[0]

def takeSecond(elem):
    return elem[1]


def acceptProbability(i, it):
    if i == 0:
        return 0.1
    else:
        return 0.995 ** it

def randomSolution():
    #obliczanie losowego rozwiązania
    x = []
    for j in range(n):
        x.append(j)

    random.shuffle(x)
    return x

def checkSolution(x, tablep, tabled):
    #funkcji obliczających wartości obu kryteriów (tzn. wartość funkcji celu jest parą liczb)
    C = generateHarmonogram(x, tablep)

    #Makespan
    makespan = max(C)

    #MaxTardiness
    scoresMaxTardiness = []
    count = 0
    for j in x:
        scoresMaxTardiness.append(max(C[count]-tabled[j],0))
        count += 1
    maxTardiness = max(scoresMaxTardiness)
    maxTotalTardiness = sum(scoresMaxTardiness)
    return makespan, maxTardiness, maxTotalTardiness

def generateHarmonogram(x, tablep):
    #funkcji obliczającej harmonogram(wartości Cij)
    result = []

    C = []
    C = [0 for i in range(3)]

    firstTask = True
    for j in x:
        for i in range(3):

            if i == 0 and firstTask:
                C[i] = tablep[i][j]
            elif i == 0 and not(firstTask):
                C[i] = C[i] + tablep[i][j]
            elif i > 0 and firstTask:
                C[i] = C[i-1] + tablep[i][j]
            elif i > 0 and not(firstTask):
                C[i] = max(C[i-1], C[i]) + tablep[i][j]

        result.append(C[2])
        firstTask = False
    return result

def movefunction(type, x):
    #funkcji ruchu (do generacji sąsiadów, najprościej wykorzystać sąsiedztwa insert lub swap),
    array = x.copy()

    if type == "insert":
        a = random.randint(0, n-1)
        b = 0
        while a == b:
            b = random.randint(0, n-1)

        buf = array[a]
        array[a] = array[b]
        array[b] = buf

    elif type == "swap":
        a = random.randint(0, n-1)
        b = 0
        while math.fabs(a-b) <= 1:
            b = random.randint(0, n-1)

        if (a < b):
            c = []
            for i in range(a, b):
                c.append(x[i])
            c.reverse()
            for i in range(a, b):
                x[i] = c[i-a]
        else:
            c = []
            for i in range(b, a):
                c.append(x[i])
            c.reverse()
            for i in range(b, a):
                x[i] = c[i-a]

    return array


def scalarization(makespan, maxTardiness, maxTotalTardiness):
    #obliczanie funkcji skalaryzacji
    return (makespan*c1)+(maxTardiness*c2)+(maxTotalTardiness*c3)

def main():

    arrayC = [[1,1,1],[2,3,2],[1,3,2],[3,1,2]]

    for c1,c2,c3 in arrayC:
        maxIters = [100, 200, 400, 800, 1600]
        scores = []
        
        for maxIter in maxIters:
            simplescores = []
            arrayForC = []

            for iteration in range(10):
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

                #Główna pętla programu

                it = 0

                x = randomSolution()
                makespan, maxTardiness, maxTotalTardiness = checkSolution(x, tablep, tabled)
                best = scalarization(makespan, maxTardiness, maxTotalTardiness)
                arrayForC.append([makespan, maxTardiness, maxTotalTardiness])

                while it < maxIter:
                    
                    xPrim = movefunction("insert", x)
                    makespanPrim, maxTardinessPrim, maxTotalTardinessPrim = checkSolution(xPrim, tablep, tabled)
                    scaleXPrim = scalarization(makespanPrim, maxTardinessPrim, maxTotalTardinessPrim)

                    if scaleXPrim < best:
                        x = xPrim
                        best = scaleXPrim
                        arrayForC.append([makespanPrim, maxTardinessPrim, maxTotalTardinessPrim])
                    else:
                        if random.random() < acceptProbability(1, it):
                            x = xPrim
                            best = scaleXPrim
                            arrayForC.append([makespanPrim, maxTardinessPrim, maxTotalTardinessPrim])
                    it = it+1

                simplescores.append(best)

            scores.append([np.mean(simplescores),np.std(simplescores)])
            # print("Srednie wartosci dla iteracji:"+str(maxIter))
            # arrayForC = np.array(arrayForC)
            # print("Makespan: " +str(np.mean(arrayForC[:][0]))+" ("+str(np.std(arrayForC[:][0]))+")")
            # print("MaxTardiness: " +str(np.mean(arrayForC[:][1]))+" ("+str(np.std(arrayForC[:][1]))+")")
            # print("MaxTotalTardiness: " +str(np.mean(arrayForC[:][2]))+" ("+str(np.std(arrayForC[:][2]))+")")


        #Wyprintowanie wyników
        for k in range(len(maxIters)):
            print("Dla "+str(maxIters[k])+" iteracji, s= " +str(scores[k][0])+", std= "+str(scores[k][1]))

        #Tworzenie wykresu
        scoresnp = np.array(scores)
        plt.plot(maxIters, scoresnp[:, 0])
        plt.grid(True)
        plt.xlabel("MaxIter")
        plt.ylabel("s(x)")
        plt.title("Wykresu wartości s(x) w zależności od liczby iteracji: c1=" +str(c1)+", c2="+str(c2)+", c3="+str(c3))
        plt.legend()
        plt.savefig(".\WykresS"+str(c1)+str(c2)+str(c3)+".jpg", dpi=72)
        plt.show()
    
main()
