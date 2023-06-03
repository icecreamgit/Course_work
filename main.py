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
    x_Middle = 0.
    for stepj in range(n):
        x_Middle += x[stepj]
    return x_Middle * (1. / float(n))

def sPowerOfTwo(x):
    # Сюда я передаю определённый столбец х текущей иттерации по i
    n = len(x)
    xCounter = 0.
    for stepj in range(n):
        xCounter += pow(x[stepj] - xMiddle(x), 2)
    return (1. / (n - 1)) * xCounter

def destrNeimanPirson(destrParam, N, k, Volume):
    hDistr = []
    for _ in range(N):

        xDestr = np.array([NormalDestib(destrParam[stepi], Volume) for stepi in range(k)])
        hMult, hSum = 1, 0

        for stepi in range(k):
            hMult *= sPowerOfTwo(xDestr[stepi])
            hSum += sPowerOfTwo(xDestr[stepi])
        hSum = (1. / float(k)) * hSum / pow(hMult, (1. / float(k)))
        hDistr.append(hSum)
    return hDistr

def MonteKarlo(alpha, k, Volume, nKarlo, Distr):
    m = 0
    MainParam = [[0., 1.] for _ in range(k)]
    M = int(alpha * nKarlo)
    for _ in range(nKarlo):
        MainKarlo = destrNeimanPirson(MainParam, 1, k, Volume)
        if MainKarlo[0] > Distr[M - 1]:
            m += 1
    return float(m) / float(nKarlo)

def Vij(Param, Volume, k):
    MainDistr = np.array([NormalDestib(Param[stepi], Volume) for stepi in range(k)])
    n = float(Volume)

    vBig = []
    for stepi in range(k):
        vSmall = []
        for stepj in range(Volume):
            vSmall.append((((n - 1.5) * n * pow((MainDistr[stepi][stepj] - xMiddle(MainDistr[stepi])), 2)
                            - 0.5 * sPowerOfTwo(MainDistr[stepi]) * (n - 1)) / ((n - 1) * (n - 2))))
        vBig.append(vSmall)
    return np.array(vBig)

def countN(k, Volume):
    N = 0
    for _ in range(k):
        N += Volume

    return N
def vMiddle(v):
    # Подаю одну строку v
    vmiddle = 0.
    n = len(v)
    for step_j in range(n):
        vmiddle += v[step_j]
    return (1. / float(n)) * vmiddle
def vTwiceMiddle(v, k, Volume):
    # Подаю всю матрицу v
    N = countN(k, Volume)
    vBig = 0.
    for stepi in range(k):
        for stepj in range(Volume):
            vBig += v[stepi][stepj]
    return (1. / float(N)) * vBig

def destrOBrien(destrParam, N, k, Volume):
    n = float(Volume)
    M = countN(k, Volume)
    vCounter = []
    for _ in range(N):
        a, b = 0., 0.
        vStart = Vij(destrParam, Volume, k)
        for stepi in range(k):
            a += pow((vMiddle(vStart[stepi]) - vTwiceMiddle(vStart, k, Volume)), 2)
            for stepj in range(Volume):
                b += pow((vStart[stepi][stepj] - vMiddle(vStart[stepi])), 2)
        a *= n * (1. / (k - 1))
        b *= (1. / (M - k))
        vCounter.append(a / b)
    return np.array(vCounter)

def mainNeimanPirson(k, volume, N, nMonteKarlo, alpha):
    MainParam = [[0., 1.] for _ in range(k)]
    MainDistr = destrNeimanPirson(MainParam, N, k, volume)

    writeFile(MainDistr, N, 'Нейман-Пирсон.dat')
    print("\nЗначение статистики Неймана-Пирсона:\n", sum(MainDistr))

    # Монте-Карло:
    resMonteKarlo = MonteKarlo(alpha, k, volume, nMonteKarlo, MainDistr)
    print("\nЗначение p-value по Монте-Карло для Неймана-Пирсона:\n", resMonteKarlo)
    if resMonteKarlo >= alpha:
        print("\nГипотеза о согласии не отвергается\n")
    else:
        print("\nГипотеза о согласии отвергается\n")

def mainBrien(k, volume, N, nMonteKarlo, alpha):
    # MainParam = [[0., 1.] for _ in range(k)]
    MainParam = [[0., 1.2], [0., 1.3]]
    MainDistr = destrOBrien(MainParam, N, k, volume)
    print("\nMainDistr:\n", MainDistr)

    writeFile(MainDistr, N, 'ОБрайан.dat')
    print("\nЗначение статистики ОБрайанa:\n", sum(MainDistr))

    # Монте-Карло:
    resMonteKarlo = MonteKarlo(alpha, k, volume, nMonteKarlo, MainDistr)
    print("\nЗначение p-value по Монте-Карло для Неймана-Пирсона:\n", resMonteKarlo)
    if resMonteKarlo >= alpha:
        print("\nГипотеза о согласии не отвергается\n")
    else:
        print("\nГипотеза о согласии отвергается\n")
def main():
    K, volume, N, NMonteKarlo, Alpha = 2, 10, 16600, 10000, 0.1
    # mainNeimanPirson(K, volume, N, NMonteKarlo, Alpha)
    mainBrien(K, volume, N, NMonteKarlo, Alpha)


if __name__ == '__main__':
    main()
