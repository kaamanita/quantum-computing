############################################################
#
# Author: Prachya Boonkwan
# Affiliation: SIIT, Thammasat Univeristy
# License: CC-BY-NC 4.0
#
############################################################

import pennylane as qml
from pennylane import numpy as np

dev = qml.device('default.qubit', wires=[0,1,2,3,4,5])

########################################

@qml.qnode(dev)
def circuit():
    # Prepare wires[0,1] = |00> + |11>
    qml.H(wires=[0])
    qml.CNOT(wires=[0,1])
    
    # Preapre wires[2,3] = |00> + i|11>
    qml.H(wires=[2])
    qml.ctrl(qml.Y(wires=[3]), control=[2])
    
    # Compute wires[0,1] AND wires[2,3]
    qml.Toffoli(wires=[0,2,4])
    qml.Toffoli(wires=[1,3,5])
    
    # Expect |000000> + |001100> + i|110000> + i|111111>
    return qml.state()

########################################

def main():

    print('The complex amplitudes for [000000, ..., 111111] are:')
    print(circuit())

########################################

if __name__ == '__main__':
    main()
