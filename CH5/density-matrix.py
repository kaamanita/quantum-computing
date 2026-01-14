############################################################
#
# Author: Prachya Boonkwan
# Affiliation: SIIT, Thammasat Univeristy
# License: CC-BY-NC 4.0
#
############################################################

import pennylane as qml
from pennylane import numpy as np
from pennylane import math as qmath    # We need this qmath, too

########################################

# Depolarization channel
def noisy_dm(mat, p_noise):

    noise = p_noise / 2 * np.eye(2)
    new_mat = (1 - p_noise) * mat + noise
    return new_mat

########################################

def main():

    # Convert a state vector into a density matrix (dm)
    mat = qmath.dm_from_state_vector([0.9, 0.1])
    mat = mat / qmath.norm(mat)

    for p_noise in range(10):
        noisy_mat = noisy_dm(mat, p_noise * 0.1)    # Noisy matrix with noise parameter
        f = qmath.fidelity(mat, noisy_mat)          # Fidelity of quantum states
        print(f'p_noise = {p_noise * 0.1:4.2f}: fidelity = {f:6.4f}')

########################################

if __name__ == '__main__':
    main()
