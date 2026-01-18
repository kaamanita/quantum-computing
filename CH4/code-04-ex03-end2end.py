############################################################
#
# Author: Prachya Boonkwan
# Affiliation: SIIT, Thammasat Univeristy
# License: CC-BY-NC 4.0
#
############################################################

import pennylane as qml
from pennylane import numpy as np

# End-to-end simulation with 1000 shots
dev = qml.device('default.qubit', wires=[0, 1], shots=1000)    # shots = number of samples

########################################

@qml.qnode(dev)
def circuit(theta: float):

    qml.RY(theta, wires=[0])
    qml.CNOT(wires=[0,1])
    qml.RZ(theta, wires=[1])
    
    # Simulation
    return qml.counts()

########################################

def main():

    print('The sample counts for output states [00, 01, 10, 11] are:')
    print(circuit(np.pi / 3))

########################################

if __name__ == '__main__':
    main()
