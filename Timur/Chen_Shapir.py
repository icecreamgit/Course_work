import math
import re

import scipy
import scipy.stats as sps
import numpy as np
from PyPDF2 import PdfReader


def readFile():
    reader = PdfReader("laplasetable2.pdf")
    a = 1
    number_of_pages = len(reader.pages)
    page = reader.pages[0]
    texts = (page.extract_text()).split()
    text = (re.findall(r'\d*\,\d+|\d+', str(texts)))
    for i in range(len(text)):
        text[i] = text[i].replace(",", ".")
    text = [float(i) for i in text]
    return text

def write_In_File(Distr, N, name, n):
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
    for i in range(int(n)):
        x += pow(f[i] - xmiddle, 2)
    x = math.sqrt((1. / (n - 1.)) * x)
    return x

def F(i, n, F0):
    masX, masF, saver = [], [], []
    eps, res = 0.01, 0.
    for j in range(len(F0)):
        if j % 2 == 0:
            masX.append(F0[j])
        elif j % 2 != 0:
            masF.append(F0[j])

    coef = (i - 3. / 8.) / (n + 1. / 4.)
    valueForCompare = round(abs(coef - 0.5), 4)
    for j in range(len(masF)):
        a = round(abs(valueForCompare - masF[j]), 4)
        if a <= eps:
            res = masX[j]
            break
    return res
def sum_Coefficient(xi, n, F0):
    sum, eps = 0., 0.0001
    for i in range(n):
        if (i + 1) > (n - 1):
           sum += (xi[n - 1] - xi[i]) / (pow(F(i + 2, n, F0), -1) - pow(F(i + 1, n, F0), -1))
        else:
            y = xi[i + 1] - xi[i]
            a = pow(F(i + 2, n, F0) + eps, -1)
            b = pow(F(i + 1, n, F0) + eps, -1)
            z = a - b
            sum += y / z
    return sum
def QN(n, N):
    valueF0 = readFile()
    saver = []
    # for i in range(N):
    xi = sorted(np.random.normal(0., 1., n))
    qn = 1. / (sCount(xi, n, xMiddle(xi, n)) * (n - 1.)) * sum_Coefficient(xi, n, valueF0)
    saver.append(np.sqrt(n) * (1 - qn))
    print(saver)
    return saver
def main():
    n, N = 10, 1000
    Distr = (QN(n, N))
    # write_In_File(Distr, N, "Чен-Шапир", n)

main()