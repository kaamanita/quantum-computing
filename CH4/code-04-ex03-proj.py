############################################################
#
# Author: Prachya Boonkwan
# Affiliation: SIIT, Thammasat Univeristy
# License: CC-BY-NC 4.0
#
############################################################

import pennylane as qml
from pennylane import numpy as np

dev = qml.device('default.qubit', wires=[0, 1])

########################################

@qml.qnode(dev)
def circuit(theta: float):

    qml.RY(theta, wires=[0])
    qml.CNOT(wires=[0,1])
    qml.RZ(theta, wires=[1])
    
    # Projective measurement
    return qml.probs()

########################################

def main():

    print('The probability distribution of [00, 01, 10, 11] is:')
    print(circuit(np.pi / 3))

########################################

if __name__ == '__main__':
    main()
