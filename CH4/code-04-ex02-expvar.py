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
    
    # Expectation of each wire
    return ( qml.expval(qml.Z(wires=[0])), qml.expval(qml.Z(wires=[1])),
             qml.var(qml.Z(wires=[0])), qml.var(qml.Z(wires=[1])) )

########################################

def main():
    
    (expz0, expz1, varz0, varz1) = circuit(np.pi / 3)
    print('The expectation on Z[0] and Z[1] are:')
    print((expz0, expz1))
    print('The variance of Z[0] and Z[1] are:')
    print((varz0, varz1))

########################################

if __name__ == '__main__':
    main()
