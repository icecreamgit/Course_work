import scipy.stats as sps
import numpy as np


def normalDestribution(xi, params):
    return sps.norm(loc=params[0], scale=params[1]).cdf(xi)

def Dminus_n(xi, params, n):
    Dlocal = []
    for i in range(n):
        Dlocal.append(normalDestribution(xi, params) - (i - 1) / n)
    return max(Dlocal)


def main():
    volume, params = 100, [0., 1.]  # params = [loc= something value, scale= something value]
    xi = np.random.normal(loc=0., scale=1., size=volume)
    Dminus_n(xi, params, n=volume)


if __name__ == "main":
    main()