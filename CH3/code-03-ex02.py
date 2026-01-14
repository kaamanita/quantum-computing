import pennylane as qml
from pennylane import numpy as np

dev = qml.device('default.qubit', wires=[0,1,2])

########################################

@qml.qnode(dev)
def circuit():

    # State preparation
    qml.H(wires=[0])
    qml.CNOT(wires=[0,1])
    qml.X(wires=[1])
    qml.CNOT(wires=[1,2])
    qml.S(wires=[2])

    # Measurement
    return qml.state()

########################################

def main():

    print('The complex amplitudes of [000, 001, 010, 011, 100, 101, 110,111] are:')
    print(circuit())

########################################

if __name__ == '__main__':
    main()
