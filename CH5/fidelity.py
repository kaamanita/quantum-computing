import pennylane as qml
from pennylane import numpy as np
from pennylane import math as qmath

########################################

# Phase damping channel
def noisy_vec(vec, p_noise):

    noise = np.array([ [0.0, 1 - p_noise],
                       [1 - p_noise, 0.0] ])
    new_vec = noise @ vec
    return new_vec

########################################

def main():

    vec = np.array([1.0, 1.0])
    vec = vec / qmath.norm(vec)
    
    for p_noise in range(10):
        new_vec = noisy_vec(vec, p_noise * 0.1)         # Noisy vector with noise parameter
        f = qmath.fidelity_statevector(vec, new_vec)    # Fidelity of quantum states
        print(f'p_noise = {p_noise * 0.1:4.2f}: fidelity = {f:6.4f}')

########################################

if __name__ == '__main__':
    main()
