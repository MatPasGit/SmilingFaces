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


#DWA PIERWSZE KRYTERIA: 1 (makespan), 3 (max tardiness), 4 (total tardiness), 5 (max lateness)
# Makespan - czas zakończenia wszystkich zadań
# Max tardiness - maksymalne spóźnienie zadania
# Total tardiness - suma spóźnień zadań
# Max lateness - maksymalna nieterminowość zadania

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
    scoresMaxLateness = []
    count = 0
    for j in x:
        scoresMaxTardiness.append(max(C[count]-tabled[j], 0))
        scoresMaxLateness.append(C[count]-tabled[j])
        count += 1
    maxTardiness = max(scoresMaxTardiness)

    #TotalTardiness
    maxTotalTardiness = sum(scoresMaxTardiness)

    #Max lateness
    maxLateness = max(scoresMaxLateness)

    return makespan, maxTardiness, maxTotalTardiness, maxLateness


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


def domination(makespan, maxTardiness, maxTotalTardiness, maxLateness, makespanPrim, maxTardinessPrim, maxTotalTardinessPrim, maxLatenessPrim):
    #obliczanie funkcji dominacji
    if (makespanPrim <= makespan) and (maxTardinessPrim <= maxTardiness) and (maxTotalTardinessPrim <= maxTotalTardiness) and (maxLatenessPrim <= maxLateness):
        if (makespanPrim < makespan) or (maxTardinessPrim < maxTardiness) or (maxTotalTardinessPrim < maxTotalTardiness) or (maxLatenessPrim < maxLateness):
            return True
    return False


def frontParetoF(P, tablep, tabled):

    F = []
    Fscore = []
    for a in P:
        makespan, maxTardiness, maxTotalTardiness, maxLateness = checkSolution(a, tablep, tabled)
        zmienna = True
        for b in P:
            if not(np.array_equiv(a, b)):
                makespanPrim, maxTardinessPrim, maxTotalTardinessPrim, maxLatenessPrim = checkSolution(b, tablep, tabled)
                if domination(makespan, maxTardiness, maxTotalTardiness, maxLateness, 
                              makespanPrim, maxTardinessPrim, maxTotalTardinessPrim, maxLatenessPrim):
                    zmienna = False
            if zmienna == False:
                break
        if zmienna:
            F.append(a)
            Fscore.append([makespan, maxTardiness, maxTotalTardiness, maxLateness])
    return F, Fscore


def main():

    maxIters = [100, 200, 400, 800, 1600]

    for iteration in range(10):
        FscoresAll = []
        FscoresDivided = []

        for maxIter in maxIters:
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

            P = []
            Pscores = []
            it = 0

            x = randomSolution()
            makespan, maxTardiness, maxTotalTardiness, maxLateness = checkSolution(x, tablep, tabled)
            P.append(x)
            Pscores.append([makespan, maxTardiness, maxTotalTardiness, maxLateness])

            while it < maxIter:

                xPrim = movefunction("insert", x)
                makespanPrim, maxTardinessPrim, maxTotalTardinessPrim, maxLatenessPrim = checkSolution(
                    xPrim, tablep, tabled)

                boolResult = domination(makespan, maxTardiness, maxTotalTardiness, maxLateness,
                                        makespanPrim, maxTardinessPrim, maxTotalTardinessPrim, maxLatenessPrim)

                if boolResult:
                    x = xPrim
                    makespan = makespanPrim
                    maxTardiness = maxTardinessPrim
                    maxTotalTardiness = maxTotalTardinessPrim
                    maxLateness = maxLatenessPrim
                    P.append(x)
                    Pscores.append([makespan, maxTardiness, maxTotalTardiness, maxLateness])
                else:
                    if random.random() < acceptProbability(1, it):
                        x = xPrim
                        makespan = makespanPrim
                        maxTardiness = maxTardinessPrim
                        maxTotalTardiness = maxTotalTardinessPrim
                        maxLateness = maxLatenessPrim
                        P.append(x)
                        Pscores.append([makespan, maxTardiness, maxTotalTardiness, maxLateness])
                it = it+1

            #Pareto
            F, Fscores = frontParetoF(P, tablep, tabled)
            #print(F)
            print(Fscores)

            arraytovisualisation = []
            for i in range(3):
                if i < len(F):
                    arraytovisualisation.append(Fscores[i].copy())
                else:
                    xPrim = movefunction("insert", F[0])
                    makespan, maxTardiness, maxTotalTardiness, maxLateness = checkSolution(xPrim, tablep, tabled)
                    arraytovisualisation.append([makespan, maxTardiness, maxTotalTardiness, maxLateness])

            x = randomSolution()
            makespan, maxTardiness, maxTotalTardiness, maxLateness = checkSolution(x, tablep, tabled)
            arraytovisualisation.append([makespan, maxTardiness, maxTotalTardiness, maxLateness])
            print(arraytovisualisation)
            #Zakresy z Fscores i arraytovisualisation
            zakresy = []
            Fscores = np.array(Fscores)
            arraytovisualisation = np.array(arraytovisualisation)
            for i in range(4):
                dolny = min(min(Fscores[:,i]), min(arraytovisualisation[:,i]))
                gorny = max(max(Fscores[:, i]), max(arraytovisualisation[:,i]))
                zakresy.append([dolny, gorny])

            print(zakresy)

            #Wizualizacje

            #Metoda 1 (bar plots)

            #Metoda 2 (value paths)

            #Metoda 4 (star cordinate system)

            #Metoda 7 (Chernoff faces)

main()
