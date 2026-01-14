import numpy as np
import numpy.random as rnd

def prepare_primes(n):
    flags = np.ones(n, dtype=bool)
    flags[0] = flags[1] = False
    for i in range(2, n):
        if flags[i]:
            for j in range(2 * i, n, i):
                flags[j] = False
    return np.arange(n)[flags]

def factorize(n, primes):
    if n == 1: return np.array([n])
    potential_factors = primes[primes <= np.sqrt(n)]
    for a in potential_factors:
        k = np.gcd(n, a)
        if k != 1:
            return np.hstack([ factorize(k, primes), factorize(n // k, primes) ])
    return np.array([n])

primes = prepare_primes(200)
print(factorize(152, primes))    # Expected result: [ 2  2  2 19]
