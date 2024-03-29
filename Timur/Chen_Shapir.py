import math
import re

import scipy
import scipy.stats as sps
import numpy as np
from PyPDF2 import PdfReader


def readFile():
    masX = []
    masF0 = []
    with open("F0.txt", 'r') as file:
        for i in file:
            lineSplit = i.split()
            masX.append(float(lineSplit[0]))
            masF0.append(float(lineSplit[1]))
    return masX, masF0

def write_In_File_Distr(Distr, N, name, n):
    with open(name + '_' + str(n) + '_' + str(N) + '.dat', 'w') as file:
        file.write(name + '(создано не ISW) N=' + str(N) + '\t n = ' + str(n) +  ' ' + '\n')
        file.write(str('0 ' + ' ' + str(N) + '\n'))
        for i in range(N):
            file.write(str(Distr[i]) + '\n')

def xMiddle(data, n):
    x_middle = 0.
    for i in range(int(n)):
        x_middle += data[i]
    x_middle = (1. / n) * x_middle
    return x_middle
def sCount(f, n, xmiddle):
    x = 0.
    for i in range(n):
        x += pow(f[i] - xmiddle, 2)
    x = math.sqrt((1. / (n - 1.)) * x)
    return x

def F(i, n, x0, F0):
    saver = []

    valueForCompare = (i - 3. / 8.) / (n + 1. / 4.)

    for j in range(len(F0)):
        saver.append(abs(valueForCompare - F0[j]))
    saverMin = min(saver)
    for j in range(len(F0)):
        if saverMin == saver[j]:
            res = x0[j]
    return res
def sum_Coefficient(xi, n, x0, F0):
    sum = 0.
    for i in range(n):
        if (i + 1) > (n - 1):
           sum += (xi[n - 1] - xi[i]) / (pow(F(i + 2, n, x0, F0), 1) - (pow(F(i + 1, n, x0, F0), 1)))
        else:
            sum += (xi[i + 1] - xi[i]) / (pow(F(i + 2, n, x0, F0), 1) - (pow(F(i + 1, n, x0, F0), 1)))
    return sum
def QN(n, N):
    masX, masF0 = readFile()
    saver = []
    for i in range(N):
        xi = sorted(np.random.normal(0., 1., n))
        qn = 1. / (sCount(xi, n, xMiddle(xi, n)) * (n - 1.)) * sum_Coefficient(xi, n, masX, masF0)
        saver.append(np.sqrt(n) * (1. - qn))
        print(i)
    return saver
def main():
    n, N = 100, 16600
    Distr = (QN(n, N))
    write_In_File_Distr(Distr, N, "Чен-ШапирQnx", n)

main()