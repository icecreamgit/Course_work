import numpy as np


def writeFile(Distr, N, name):
    with open(name, 'w') as file:
        file.write(name + '(создан моей программой) N=' + str(N) + ' ' + '\n')
        file.write(str('0 ' + ' ' + str(N) + '\n'))
        for i in range(N):
            file.write(str(Distr[i]) + '\n')

def NormalDestib(Params, Volume):
    return np.random.normal(loc=Params[0], scale=Params[1], size=Volume)

def xMiddle(x):
    # Сюда я передаю определённый столбец х текущей иттерации по i
    n = len(x)
    x_Middle = 0
    for stepj in range(n):
        x_Middle += x[stepj]
    return (x_Middle * (1. / float(n)))

def sPowerOfTwo(x):
    # Сюда я передаю определённый столбец х текущей иттерации по i
    n = len(x)
    xCounter = 0
    for stepj in range(n):
        xCounter += pow(x[stepj] - xMiddle(x), 2)
    return ((1. / (20 - 1)) * xCounter)

def destrNeimanPirson(destrParam, N, k, Volume):
    hDistr = []
    for _ in range(N):

        xDestr = np.array([NormalDestib(destrParam[stepi], Volume) for stepi in range(k)])
        hMult, hSum = 1, 0

        for stepi in range(k):
            hMult *= sPowerOfTwo(xDestr[stepi])
            hSum += sPowerOfTwo(xDestr[stepi])
        hSum = (1. / float(k)) * hSum / pow(hMult, (1. / float(k)))
        print("\nhSum:\n", hSum)
        hDistr.append(hSum)
    return hDistr

def main():
    # Подаю на вход 2 текстовых файла, просматриваю их в функции Open
    k, volume, N, nMonteKarlo, m, alpha = 2, 10, 16600, 10000, 0, 0.1

    MainParam = [[0., 1.] for _ in range(k)]
    MainDistr = destrNeimanPirson(MainParam, N, k, volume)

    writeFile(MainDistr, N, 'Нейман-Пирсон.dat')
    print("\nЗначение статистики Неймана-Пирсона:\n", sum(MainDistr))

    # Монте-Карло:
    volume = int(alpha * volume)
    MainKarlo = destrNeimanPirson(MainParam, nMonteKarlo, k, volume)
    for _ in range(nMonteKarlo):
        if MainKarlo[_] > MainDistr[_]:
            m += 1
    print("\nЗначение по Монте-Карло:\n", float(m) / float(nMonteKarlo))



if __name__ == '__main__':
    main()


