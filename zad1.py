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

    return makespan, maxTardiness

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

def domination(makespan, maxTardiness, makespanPrim, maxTardinessPrim):
    #obliczanie funkcji dominacji
    if (makespanPrim <= makespan) and (maxTardinessPrim <= maxTardiness):
        if (makespanPrim < makespan) or (maxTardinessPrim < maxTardiness):
            return True
    return False

def frontParetoF(P, tablep, tabled):

    F = []
    Fscore = []
    for a in P:
        makespan, maxTardiness = checkSolution(a, tablep, tabled)
        zmienna = True
        for b in P:
            if not(np.array_equiv(a, b)):
                makespanPrim, maxTardinessPrim = checkSolution(b, tablep, tabled)
                if domination(makespan, maxTardiness, makespanPrim, maxTardinessPrim):
                    zmienna = False
            if zmienna == False:
                break
        if zmienna:
            F.append(a)
            Fscore.append([makespan, maxTardiness])
    return F, Fscore

def calculateHVI(Z, array):

    if len(array) == 3:
        a = Z[0] - array[1][0]
        b = Z[1] - array[1][1]
        return a*b
    else:
        area = 0
        A = Z.copy()
        for i in range(len(array)):
            if i == 0:
                continue
            elif i == len(array)-1:
                continue
            else:
                a = A[0] - array[i][0]
                b = A[1] - array[i][1]
                area = area + a*b
                A[1] = array[i][1]
        return area

def main():

    maxIters = [100, 200, 400, 800, 1600]
    HVIscores = []

    for iteration in range(10):
        FscoresAll=[]
        FscoresDivided=[]

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
            makespan, maxTardiness = checkSolution(x, tablep, tabled)
            P.append(x)
            Pscores.append([makespan, maxTardiness])

            while it < maxIter:
                
                xPrim = movefunction("insert", x)
                makespanPrim, maxTardinessPrim = checkSolution(xPrim, tablep, tabled)

                boolResult = domination(makespan, maxTardiness,
                                        makespanPrim, maxTardinessPrim)

                if boolResult:
                    x = xPrim
                    makespan = makespanPrim
                    maxTardiness = maxTardinessPrim
                    P.append(x)
                    Pscores.append([makespan, maxTardiness])
                else:
                    if random.random() < acceptProbability(1, it):
                        x = xPrim
                        makespan = makespanPrim
                        maxTardiness = maxTardinessPrim
                        P.append(x)
                        Pscores.append([makespan, maxTardiness])
                it = it+1

            #Pareto
            F, Fscores = frontParetoF(P, tablep, tabled)

            #Wykresy P i F
            print(str(iteration)+", "+str(maxIter))

            #print(Pscores)
            #print(Fscores)

            Fscores.sort(key=takeSecond)
            #print(Fscores)
            Fscores.sort(key=takeFirst)
            #print(Fscores)

            FscoresAll.extend(Fscores.copy())
            FscoresDivided.append(Fscores.copy())

            Pscores = np.array(Pscores)
            Fscores = np.array(Fscores)

            x = Pscores[:, 0]
            y = Pscores[:, 1]
            plt.scatter(x, y, label="P", c="b")

            x = Fscores[:, 0]
            y = Fscores[:, 1]
            plt.plot(x, y, 'ro-', label="F")

            plt.grid(True)
            plt.xlabel("Makespace")
            plt.ylabel("MaxTardiness")
            plt.title("Wykresu zbioru i frontu Pareto dla dwóch kryteriów - iter: "+str(iteration)+", maxIter: "+str(maxIter))
            plt.legend()
            plt.savefig(".\Zad1\WykresPareto"+str(maxIter)+"iter"+str(iteration)+".jpg", dpi=72)
            #plt.show()
            plt.close()
            plt.cla()
            plt.clf()
        
        #Wykresy HVI
        
        FscoresAll.sort(key=takeSecond)
        FscoresAll.sort(key=takeFirst)
        FscoresAll = np.array(FscoresAll)
        Z = [max(FscoresAll[:, 0]), max(FscoresAll[:, 1])]

        plt.scatter(Z[0], Z[1], label="Z", c="b")

        for k in range(len(maxIters)):
            array = FscoresDivided[k]
            #print(array)
            temp = []
            array.sort(key=takeFirst)
            temp.append([array[0][0],Z[1]])
            temp.append([Z[0], array[-1][1]])
            #print(temp)
            array.extend(temp)
            array.sort(key=takeSecond)
            array.sort(key=takeFirst)
            array = np.array(array)
            plt.step(array[:, 0], array[:, 1], 'o-', label="Punkty - "+str(maxIters[k]))
            HVIscores.append(calculateHVI(Z, array))

        plt.grid(True)
        plt.xlabel("Makespace")
        plt.ylabel("MaxTardiness")
        plt.title("Wykresu HVI - iter: "+str(iteration))
        plt.legend()
        plt.savefig(".\Zad1\WykresHVIiter"+str(iteration)+".jpg", dpi=72)
        plt.close()
        plt.cla()
        plt.clf()
        #plt.show()
        
    #Wyniki średnie HVI
    for k in range(len(maxIters)):
        print("Dla "+str(maxIters[k])+" iteracji, HVI= " +
              str(np.mean(HVIscores[k::len(maxIters)]))+", std= "+str(np.std(HVIscores[k::len(maxIters)])))

main()
