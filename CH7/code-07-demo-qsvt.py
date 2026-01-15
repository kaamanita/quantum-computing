############################################################
#
# Author: Prachya Boonkwan
# Affiliation: SIIT, Thammasat Univeristy
# License: CC-BY-NC 4.0
#
############################################################

import pennylane as qml
from pennylane import numpy as np

target_wires = ['t1','t2']
dev = qml.device('default.qubit', wires=target_wires)

mat = np.array([ [0.7, 0.5],
                 [0.5, 0.4] ], dtype=np.complex128)

########################################

@qml.qnode(dev, shots=1000)
def circuit():
    coeffs = np.array([0.1, 0.2, 0.3])                # 0.1 + 0.2j x + 0.3 x^2
    block_encoding = qml.BlockEncode(mat, target_wires)
    projectors = [ qml.PCPhase(phase, dim=2, wires=target_wires)
                   for phase in coeffs ]
    qml.QSVT(block_encoding, projectors)
    return qml.counts(wires=target_wires)

########################################

def main():
    print('Sample counts for the final states are:')
    counts = circuit()
    print(counts)
    # Expected result:
    # '00': 957, '01': 19, '10': 20, '11': 4}

########################################

if __name__ == '__main__':
    main()
