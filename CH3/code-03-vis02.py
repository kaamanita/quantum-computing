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
    qml.H(wires=[0])
    qml.RY(theta, wires=[0])
    qml.CNOT(wires=[0,1])
    return qml.state()
    
########################################

def main():

    fig, ax = qml.draw_mpl(circuit)(np.pi / 6)
    fig.savefig('circuit.png')

########################################

if __name__ == '__main__':
    main()
