import math

import scipy.stats as sps
import numpy as np

def write_In_File(Distr, N, name, n):
    with open(name + '_' + str(n) + '_' + str(N) + '.dat', 'w') as file:
        file.write(name + '(создано не ISW) N=' + str(N) + '\t n = ' + str(n) +  ' ' + '\n')
        file.write(str('0 ' + ' ' + str(N) + '\n'))
        for i in range(N):
            file.write(str(Distr[i]) + '\n')

def xMiddle(data, n):
    x_middle = 0
    for i in range(int(n)):
        x_middle += data[i]
        x_middle = (1 / n) * x_middle
    return(x_middle)
def sCount(f, n, xmiddle):
    x = 0
    for i in range(int(n)):
        x += pow(f[i] - xmiddle, 2)
        x = math.sqrt((1 / n) * x)
    return x

def F(i, n):
    coef = (i - 3. / 8.) / (n + 1. / 4.)
    return sps.norm.cdf(coef) - 0.5
def sum_Coefficient(xi, n):
    sum = 0
    for i in range(n):
        if (i + 1) > (n - 1):
            break
           # sum += (xi[n - 1] - xi[i]) / (pow(F(n - 1, n), -1) - pow(F(i, n), -1))
        else:
            sum += (xi[i + 1] - xi[i]) / (pow(F(i, n), -1))
    return sum
def QN(n, N):
    saver = []
    for i in range(N):
        xi = sorted(np.random.normal(0., 1., n))
        saver.append(1. / (sCount(xi, n, xMiddle(xi, n))  * (n - 1.)) * sum_Coefficient(xi, n))
        print(i)
    return saver
def main():
    n, N = 10, 10000
    Distr = QN(n, N)
    write_In_File(Distr, N, "Чен-Шапир", n)


main()