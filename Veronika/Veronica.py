import scipy.stats as sps
import numpy as np

def writeFile(Distr, N, name, n):
    with open(name + '_' + str(n) + '_' + str(N) + '.dat', 'w') as file:
        file.write(name + '(создано не ISW) N=' + str(N) + '\t n = ' + str(n) +  ' ' + '\n')
        file.write(str('0 ' + ' ' + str(N) + '\n'))
        for i in range(N):
            file.write(str(Distr[i][0]) + '\n')


def normalDestributionFi(xi, params):
    return sps.norm(loc=params[0], scale=params[1]).cdf(xi)
def Dminus_n(xi, params, n):
    Dlocal = []
    for i in range(n):
        Dlocal.append(normalDestributionFi(xi[i], params) - (i - 1.) / n)
    maxValue = max(Dlocal)
    Dlocal.clear()
    return maxValue

def Dplus_n(xi, params, n):
    Dlocal = []
    for i in range(n):
        Dlocal.append(i / n - normalDestributionFi(xi[i], params))
    maxValue = max(Dlocal)
    Dlocal.clear()
    return maxValue

def multiplicationVariant(mode, n):
    if mode == 0:
        return (np.sqrt(n) + 0.155 + 0.24 / np.sqrt(n))
    elif mode == 1:
        return np.sqrt(n)

def Vn(params, n, N): # N - число испытаний, n - объём выборки
    Vnlocal = np.zeros((N, 1))
    for i in range(N):
        xi = sorted(np.random.normal(loc=0., scale=1., size=n))
        Vnlocal[i][0] = (Dplus_n(xi, params, n) + Dminus_n(xi, params, n)) * multiplicationVariant(mode=0, n=n)
        print(i)
    return Vnlocal

def main():
    volume, params, N = 100, [0., 1.], 16600  # params = [loc= something value, scale= something value]
    kuperDestributionModified = Vn(params, n=volume, N=N)

    writeFile(kuperDestributionModified, N, "Купер_0_155", volume)

# if __name__ == "main":
main()