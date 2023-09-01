import scipy.stats as sps
import numpy as np

def writeFile(Distr, N, name, n):
    with open(name + '_' + str(n) + '_' + str(N) + '.dat', 'w') as file:
        file.write(name + '(создано не ISW) N=' + str(N) + '\t n = ' + str(n) +  ' ' + '\n')
        file.write(str('0 ' + ' ' + str(N) + '\n'))
        for i in range(N):
            file.write(str(Distr[i][0]) + '\n')


def typeDestibutionFi(xi, params, type):
    if type == 'normal':
        return sps.norm(loc=params[0], scale=params[1]).cdf(xi)
    elif type == 'logistic':
        return sps.logistic(loc=params[0], scale=params[1]).cdf(xi)
    elif type == 'laplace':
        return sps.laplace(loc=params[0], scale=params[1]).cdf(xi)

def Dminus_n(xi, params, n, type):
    Dlocal = []
    for i in range(n):
        Dlocal.append(typeDestibutionFi(xi[i], params, type) - (i - 1.) / n)
    maxValue = max(Dlocal)
    Dlocal.clear()
    return maxValue

def Dplus_n(xi, params, n, type):
    Dlocal = []
    for i in range(n):
        Dlocal.append(i / n - typeDestibutionFi(xi[i], params, type))
    maxValue = max(Dlocal)
    Dlocal.clear()
    return maxValue

def multiplicationVariant(mode, n):
    if mode == 0:
        return (np.sqrt(n) + 0.155 + 0.24 / np.sqrt(n))
    elif mode == 1:
        return np.sqrt(n)
#     (np.sqrt(n)) + 1. / (3 * np.sqrt(n))

def Vn(params, n, N, type): # N - число испытаний, n - объём выборки
    Vnlocal = np.zeros((N, 1))
    for i in range(N):
        xi = sorted(np.random.normal(loc=0., scale=1., size=n))
        Vnlocal[i][0] = (Dplus_n(xi, params, n, type) + Dminus_n(xi, params, n, type)) * (np.sqrt(n)) + 1. / (3 * np.sqrt(n))
    return Vnlocal

def monteKarlo(alpha, params, n, nKarlo, Distr, type):
    m = 0
    M = int(alpha * nKarlo)
    for _ in range(nKarlo):
        mainKarlo = Vn(params=params, n=n, N=1, type=type)
        if mainKarlo[0] > Distr[M]:
            m += 1
    return m / nKarlo

def unitTest(params, n, N, type, nKarlo, alpha):
    # Тип используемого распределения, 3 вида в проге: logistic, normal, laplace
    kuperDestributionModified = Vn(params, n=n, N=N, type='normal')
    result = monteKarlo(alpha, params, n=n, nKarlo=nKarlo, Distr=kuperDestributionModified, type=type)
    if result < alpha:
        print(f'type :\t{type}\nДостигаемый уровень значимости при alpha = {alpha}\t:\t'
              f'{result}\nГипотеза отвергается')
    else:
        print(f'type :\t{type}\nДостигаемый уровень значимости при alpha = {alpha}\t:\t'
              f'{result}\nГипотеза НЕ отвергается')

def main():
    alpha, volume, params, N = 0.1, 100, [0., 1.], 16600  # params = [loc= something value, scale= something value]
    nKarlo = 1000

    # Тип используемого распределения, 3 вида в проге: logistic, normal, laplace
    for i in range(3):
        unitTest(params, volume, N, "logistic", nKarlo, alpha)
    for i in range(3):
        unitTest(params, volume, N, "normal", nKarlo, alpha)
    # writeFile(kuperDestributionModified, N, "Купер_1_sqrt", volume)

main()