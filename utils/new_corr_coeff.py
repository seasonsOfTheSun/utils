
# implements "A NEW COEFFICIENT OF CORRELATION"
# from an eponymous 2020 paper by one S. Chatterjee
# can be found at: https://arxiv.org/pdf/1909.10140.pdf

import numpy as np
import scipy.stats

x = np.random.randint(10,size=(300,))
y = np.random.randint(10,size=(300,))


def chatterjee_coeff(x,y):

    assert len(x) == len(y)
    n = len(x)

    # when there are ties

    r_x = scipy.stats.rankdata(x, method='ordinal') # the rank of x, ties broken arbitrarily
    y_by_x=np.array([y[i] for i in r_x-1])# elements of y reorodered by the rank of the corresponding x

    r_y = scipy.stats.rankdata(y_by_x, method='max') # the number of elements of y that y_by_x[i] is greater than or equal to.
    l_y = n - (scipy.stats.rankdata(y_by_x, method='min')-1) # the number of elements of y that y_by_x[i] is less than or equal to.

    i = np.random.randint(30)
    assert r_y[i] == sum([y_by_x[i] >= y[j] for j in range(n)])
    assert l_y[i] == sum([y_by_x[i] <= y[j] for j in range(n)])

    numerator =   n * np.sum(np.abs(r_y[:-1]-r_y[1:]))
    denominator = 2 * np.sum(l_y * (n - l_y))

    return numerator/denominator


print(chatterjee_coeff(x,y))
