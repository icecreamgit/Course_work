import scipy.stats as sps
import numpy as np

def writeFile(Distr, N, name):
    with open(name, 'w') as file:
        file.write(name + '(создано не ISW) N=' + str(N) + ' ' + '\n')
        file.write(str('0 ' + ' ' + str(N) + '\n'))
        for i in range(N):
            file.write(str(Distr[i][0]) + '\n')


def normalDestributionFi(xi, params):
    return sps.norm(loc=params[0], scale=params[1]).cdf(xi)

def Dminus_n(xi, params, n):
    Dlocal = []
    for i in range(n):
        Dlocal.append(normalDestributionFi(xi[i], params) - (i - 1.) / n)
    return max(Dlocal)

def Dplus_n(xi, params, n):
    Dlocal = []
    for i in range(n):
        Dlocal.append(i / n - normalDestributionFi(xi[i], params))
    return max(Dlocal)

def Vn(params, n, N): # N - число испытаний, n - объём выборки
    Vnlocal = np.zeros((N, 1))
    for i in range(N):
        xi = sorted(np.random.normal(loc=0., scale=1., size=n))
        Vnlocal[i][0] = Dplus_n(xi, params, n) + Dminus_n(xi, params, n)
        print(i)
    return Vnlocal

def main():
    volume, params, N = 10, [0., 1.], 1000  # params = [loc= something value, scale= something value]
    kuperDestributionModified = Vn(params, n=volume, N=N) * (np.sqrt(volume) + 0.155 + 0.24 / np.sqrt(volume))

    writeFile(kuperDestributionModified, N, "Купер.dat")

# if __name__ == "main":
main()