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

    print(qml.draw(circuit)(np.pi / 6))

########################################

if __name__ == '__main__':
    main()
