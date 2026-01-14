import pennylane as qml
from pennylane import numpy as np

# Step-by-step simulation by 10-shots sampling
dev = qml.device('default.qubit', wires=[0, 1], shots=10)    # shots = number of samples

########################################

@qml.qnode(dev)
def circuit(theta: float):

    qml.RY(theta, wires=[0])
    qml.CNOT(wires=[0,1])
    qml.RZ(theta, wires=[1])
    
    # Sampling
    return qml.sample()

########################################

def main():
    print('10 output samples from the circuit are:')
    print(circuit(np.pi / 3))

########################################

if __name__ == '__main__':
    main()
