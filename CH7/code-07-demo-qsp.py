############################################################
#
# Author: Prachya Boonkwan
# Affiliation: SIIT, Thammasat Univeristy
# License: CC-BY-NC 4.0
#
############################################################

import pennylane as qml
from pennylane import numpy as np

control_wires = ['c']
target_wires = ['t1', 't2', 't3']
dev = qml.device('default.qubit', wires=target_wires + control_wires)

########################################

@qml.prod        # Make this function an operator argument
def my_opr(wires):
    qml.Hadamard(wires=wires[0])
    qml.X(wires=wires[2])
    qml.CNOT(wires=[wires[0], wires[1]])
    qml.CNOT(wires=[wires[0], wires[2]])

########################################

@qml.qnode(dev, shots=1000)
def circuit():
    coeffs = np.array([0.1, 0.2j, 0.3])                    # 0.1 + 0.2j x + 0.3 x^2
    phases = qml.poly_to_angles(coeffs, routine='GQSP')    # Convert the coefficients to phases
    qml.GQSP(my_opr(target_wires), phases, control=control_wires)
    return qml.counts(wires=target_wires)

########################################

def main():
    print('Sample counts for the final states are:')
    counts = circuit()
    print(counts)
    # Expected result:
    # {'000': 268, '001': 23, '011': 243, '100': 202, '110': 21, '111': 243}

########################################

if __name__ == '__main__':
    main()
