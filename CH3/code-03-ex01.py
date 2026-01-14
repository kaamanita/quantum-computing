import pennylane as qml
from pennylane import numpy as np

dev = qml.device('default.qubit', wires=[0, 1])

########################################

@qml.qnode(dev)
def circuit():

    # State preparation
    qml.H(wires=[0])          # This is the Hadamard gate
    qml.X(wires=[1])          # This is the NOT gate
    qml.S(wires=[1])          # This is the phase shift gate
    qml.CNOT(wires=[0, 1])    # This is the conditional NOT gate

    # Measurement
    return qml.state()        # Current quantum state

########################################
    
def main():

    print('The complex amplitudes for quantum states [00, 01, 10, 11] are:')
    print(circuit())

########################################

if __name__ == '__main__':
    main()
